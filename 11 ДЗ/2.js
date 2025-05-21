// Функция fetchData с имитацией асинхронного запроса
function fetchData(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url === '/users') {
        resolve([
          { id: 1, name: 'Alice' },
          { id: 2, name: 'Bob' },
          { id: 3, name: 'Charlie' }
        ]);
      } else if (url === '/user/1') {
        resolve({ id: 1, name: 'Alice', details: 'Developer' });
      } else {
        reject(new Error('Invalid URL'));
      }
    }, 2000); // Задержка 2 секунды
  });
}

// Цепочка асинхронных операций
fetchData('/users')
  .then(users => {
    console.log('Получен список пользователей:', users);
    const firstUser = users[0];
    return fetchData(`/user/${firstUser.id}`);
  })
  .then(userDetails => {
    console.log('Информация о первом пользователе:', userDetails);
  })
  .catch(error => {
    console.error('Произошла ошибка:', error.message);
  });