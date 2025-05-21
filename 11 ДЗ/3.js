// Функция delay для имитации задержки
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Асинхронная версия функции
async function fetchAndProcessData() {
  try {
    // Первый запрос
    const users = await fetchData('/users');
    console.log('Получен список пользователей:', users);

    // Добавляем задержку
    await delay(1000);

    // Второй запрос
    const firstUser = users[0];
    const userDetails = await fetchData(`/user/${firstUser.id}`);
    console.log('Информация о первом пользователе:', userDetails);
  } catch (error) {
    console.error('Произошла ошибка:', error.message);
  }
}

// Вызов функции
fetchAndProcessData();