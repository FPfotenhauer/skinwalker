(function () {
  var HERO_IMAGES = [
    "dsc_0346.jpg",
    "dsc_0386.jpg",
    "dsc_0419.jpg",
    "dsc_0420.jpg",
    "pxl_20201003_172705451.jpg",
    "pxl_20210929_133957389.jpg",
    "pxl_20231015_161657432.jpg",
    "pxl_20231015_161701004.jpg",
    "pxl_20231015_161704086.jpg",
    "pxl_20231028_135531917.jpg",
    "pxl_20231028_135535679.jpg",
    "pxl_20250721_201958529.mp.jpg",
    "pxl_20260727_104500920.mp.jpg",
    "pxl_20260727_104502441.jpg",
    "pxl_20260727_104504548.jpg",
    "pxl_20260727_104508105.jpg"
  ];

  var hero = document.getElementById("hero");
  if (!hero) return;

  var choice = HERO_IMAGES[Math.floor(Math.random() * HERO_IMAGES.length)];
  hero.style.backgroundImage =
    "linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.35)), url('img/hero/" + choice + "')";
})();
