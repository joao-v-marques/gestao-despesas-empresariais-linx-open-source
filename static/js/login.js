const form = document.getElementById("loginForm");
const btn = document.getElementById("loginBtn");

form.addEventListener("submit", () => {
    if (btn.classList.contains("loading")) return;

    btn.classList.add("loading");
    btn.disabled = true;
});