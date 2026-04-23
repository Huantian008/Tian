document.addEventListener("DOMContentLoaded", function () {
  ["localStorage", "sessionStorage"].forEach(function (storageName) {
    var storage = window[storageName];

    if (!storage) {
      return;
    }

    Object.keys(storage).forEach(function (key) {
      if (/lrc/i.test(key)) {
        storage.removeItem(key);
      }
    });
  });

  var meta = document.querySelector(".article-meta");
  var links = document.querySelectorAll(".related a");

  if (meta) {
    meta.title = "页面示例信息";
  }

  links.forEach(function (link) {
    link.setAttribute("title", link.textContent.trim());
  });
});
