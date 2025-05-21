const API_URL = "https://reqres.in/api/login "; // Пример API
const userStatus = document.getElementById("userStatus");
const logoutBtn = document.getElementById("logoutBtn");
const networkStatus = document.getElementById("networkStatus");

// Проверка токена при загрузке
window.addEventListener("load", () => {
  const token = localStorage.getItem("token");
  if (token) {
    userStatus.textContent = "Привет, пользователь";
    logoutBtn.style.display = "inline-block";
  } else {
    window.location.href = "login.html";
  }
});

// Логин
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("token", data.token);
      window.location.href = "index.html";
    } else {
      throw new Error("Неверные учетные данные");
    }
  } catch (err) {
    document.getElementById("error").textContent = err.message;
  }
});

// Выход
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "login.html";
});

// Статус сети
window.addEventListener("online", () => {
  networkStatus.textContent = "Соединение восстановлено";
});
window.addEventListener("offline", () => {
  networkStatus.textContent = "Вы в офлайне";
});