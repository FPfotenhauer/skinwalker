#!/usr/bin/env python3
"""Create a skinwalker.de post from one image and open a PR against develop."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PICS_DIR = ROOT / "pics"
SITE_INDEX = ROOT / "site" / "index.html"
GITHUB_ENV_PATH = Path("/root/.openpaw/.env-github")
MAX_TITLE_LEN = 120
MAX_TEXT_LEN = 4_000
IMAGE_EXTENSIONS = {".jpg", ".jpeg"}
MONTHS_DE = [
    "Januar",
    "Februar",
    "Maerz",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
]


@dataclass(frozen=True)
class CommandResult:
    args: list[str]
    stdout: str
    stderr: str


def run(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"{args[0]} failed: {detail}")
    return CommandResult(args=args, stdout=completed.stdout, stderr=completed.stderr)


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def github_env() -> dict[str, str]:
    env = dict(os.environ)
    values = load_env_file(GITHUB_ENV_PATH)
    token = values.get("GITHUB_TOKEN") or env.get("GITHUB_TOKEN") or env.get("GH_TOKEN")
    if not token:
        raise RuntimeError("GitHub token is not configured")
    env["GITHUB_TOKEN"] = token
    env["GH_TOKEN"] = token
    return env


def clean_text(value: str, field_name: str, max_len: int) -> str:
    text = value.strip()
    if not text:
        raise RuntimeError(f"{field_name} must not be empty")
    if len(text) > max_len:
        raise RuntimeError(f"{field_name} is too long")
    return text


def slugify(value: str) -> str:
    normalized = value.lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized[:48].strip("-") or "beitrag"


def unique_path(base: Path) -> Path:
    if not base.exists():
        return base
    stem = base.stem
    suffix = base.suffix
    for index in range(2, 100):
        candidate = base.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find a free filename for {base.name}")


def validate_source_image(path_text: str) -> Path:
    path = Path(path_text).expanduser().resolve(strict=True)
    if not path.is_file():
        raise RuntimeError("image path is not a regular file")
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        raise RuntimeError("skinwalker posts currently accept JPEG images only")
    return path


def jpeg_markers(path: Path) -> set[int]:
    data = path.read_bytes()
    if len(data) < 4 or data[0] != 0xFF or data[1] != 0xD8:
        raise RuntimeError(f"{path.name} is not a valid JPEG")
    markers: set[int] = set()
    index = 2
    while index < len(data):
        if data[index] != 0xFF:
            break
        marker = data[index + 1]
        markers.add(marker)
        if marker == 0xDA:
            break
        if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
            index += 2
            continue
        length = (data[index + 2] << 8) + data[index + 3]
        index += 2 + length
    return markers


def assert_no_exif_or_iptc(path: Path) -> None:
    stripped_markers = {0xE1, 0xED}
    if jpeg_markers(path) & stripped_markers:
        raise RuntimeError(f"{path.name} still contains EXIF/XMP/IPTC metadata")


def german_date(today: date) -> str:
    return f"{today.day}. {MONTHS_DE[today.month - 1]} {today.year}"


def post_paragraph_html(text: str) -> str:
    lines = [escape(line.strip()) for line in text.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        raise RuntimeError("Text must not be empty")
    return "<br>\n          ".join(lines)


def article_html(today: date, title: str, image_name: str, alt_text: str, text: str) -> str:
    return f"""      <article class="post">
        <p class="post-date">{escape(german_date(today))}</p>
        <h2 class="post-title">{escape(title)}</h2>
        <img
          class="post-image"
          src="img/pics/{escape(image_name)}"
          alt="{escape(alt_text)}"
          loading="lazy"
        />
        <p class="post-text">
          {post_paragraph_html(text)}
        </p>
      </article>
"""


def insert_article(article: str) -> None:
    html = SITE_INDEX.read_text(encoding="utf-8")
    marker = "      -->\n"
    index = html.find(marker)
    if index == -1:
        raise RuntimeError("Could not find post insertion marker in site/index.html")
    insert_at = index + len(marker)
    updated = html[:insert_at] + article + "\n" + html[insert_at:]
    SITE_INDEX.write_text(updated, encoding="utf-8")


def clean_worktree() -> None:
    result = run(["git", "status", "--porcelain"])
    if result.stdout.strip():
        raise RuntimeError("skinwalker worktree is not clean")


def create_branch(branch: str) -> None:
    run(["git", "fetch", "origin", "develop"])
    run(["git", "checkout", "develop"])
    run(["git", "pull", "--ff-only", "origin", "develop"])
    run(["git", "checkout", "-b", branch])


def push_branch(branch: str, env: dict[str, str]) -> None:
    run(
        [
            "git",
            "-c",
            (
                "credential.helper=!f() { echo username=x-access-token; "
                'echo password="$GITHUB_TOKEN"; }; f'
            ),
            "push",
            "-u",
            "origin",
            branch,
        ],
        env=env,
    )


def create_pr(branch: str, title: str, body: str, env: dict[str, str]) -> str:
    result = run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "develop",
            "--head",
            branch,
            "--title",
            title,
            "--body",
            body,
        ],
        env=env,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--alt")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    title = clean_text(args.title, "title", MAX_TITLE_LEN)
    text = clean_text(args.text, "text", MAX_TEXT_LEN)
    alt_text = clean_text(args.alt or f"Bild zum Beitrag: {title}", "alt", 180)
    source_image = validate_source_image(args.image)
    today = date.today()
    slug = slugify(title)
    image_target = unique_path(PICS_DIR / f"{today.isoformat()}-{slug}.jpg")
    branch = f"skinwalker-post-{today.isoformat()}-{slug}"
    result: dict[str, Any] = {
        "branch": branch,
        "image": str(image_target.relative_to(ROOT)),
        "web_image": f"site/img/pics/{image_target.stem.lower()}.jpg",
        "title": title,
        "date": today.isoformat(),
        "dry_run": args.dry_run,
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    clean_worktree()
    create_branch(branch)
    PICS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_image, image_target)
    run([sys.executable, "scripts/strip-exif.py"])
    assert_no_exif_or_iptc(image_target)
    run([sys.executable, "scripts/prepare-images.py"])
    insert_article(
        article_html(
            today,
            title,
            image_target.with_suffix(".jpg").name.lower(),
            alt_text,
            text,
        )
    )

    run(["git", "add", "pics", "site/index.html", "site/img/pics"])
    run(["git", "commit", "-m", f"Add skinwalker post: {title}"])
    env = github_env()
    push_branch(branch, env)
    pr_url = create_pr(
        branch,
        f"Add skinwalker post: {title}",
        (
            "Erstellt per Signal-Workflow.\n\n"
            "- Bild vor Commit durch `scripts/strip-exif.py` bereinigt\n"
            "- Web-Kopie durch `scripts/prepare-images.py` erzeugt\n"
            "- Beitrag in `site/index.html` ergänzt"
        ),
        env,
    )
    result["pr_url"] = pr_url
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
