# Game PC Store

Полный стек интернет-магазина по продаже игровых ПК.

## Стек

- **Backend:** FastAPI (Python), PostgreSQL, JWT, Alembic, Docker
- **Frontend:** React + TypeScript, Tailwind CSS, react-router-dom, react-beautiful-dnd
- **Тестирование:** Jest + React Testing Library
- **Docker Compose**

## Установка

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Vadim2001-04/HomeWork-Developing.git 
cd game-pc-store-fullstack

docker-compose up --build

cd backend
pytest tests/

cd frontend
npm test