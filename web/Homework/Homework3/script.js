document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("registerForm");
  var usernameInput = document.getElementById("username");
  var usernameError = document.getElementById("usernameError");
  var submitMessage = document.getElementById("submitMessage");

  function clearError() {
    usernameInput.classList.remove("input-error");
    usernameError.textContent = "";
  }

  usernameInput.addEventListener("input", function () {
    if (usernameInput.value.trim() !== "") {
      clearError();
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var username = usernameInput.value.trim();

    clearError();
    submitMessage.textContent = "";

    if (username === "") {
      usernameInput.classList.add("input-error");
      usernameError.textContent = "用户名不能为空。";
      usernameInput.focus();
      return;
    }

    submitMessage.textContent = "提交成功，欢迎你，" + username + "。";
  });

  form.addEventListener("reset", function () {
    clearError();
    submitMessage.textContent = "";
  });
});
