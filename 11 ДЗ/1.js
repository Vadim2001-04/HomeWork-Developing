// Синхронный код 1
console.log('Синхронный код 1');

// Отложенная задача через setTimeout
setTimeout(() => console.log('setTimeout 1'), 0);

// Асинхронная задача через Promise
Promise.resolve().then(() => console.log('Promise 1'));

// Синхронный код 2
console.log('Синхронный код 2');