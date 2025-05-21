from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator, Field
from typing import List, Optional
from datetime import datetime, date
import json
import re
import os

app = FastAPI()

# Путь для сохранения обращений
DATA_FILE = "appeals.json"

# Загружаем существующие обращения или создаем пустой список
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        appeals = json.load(f)
else:
    appeals = []

# Модель для причины обращения (используется в заданиях 2* и 3**)
class Reason(BaseModel):
    reason_type: str = Field(..., regex="^(нет доступа к сети|не работает телефон|не приходят письма)$")
    problem_date: date
    problem_time: str = Field(..., regex="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")

    @validator('problem_date')
    def validate_problem_date(cls, v):
        if v > date.today():
            raise ValueError("Дата обнаружения проблемы не может быть в будущем")
        return v

# Основная модель данных (задание 1)
class AppealBase(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr

    # Валидаторы для имени и фамилии
    @validator('last_name', 'first_name')
    def validate_cyrillic(cls, v):
        if not re.fullmatch(r'^[А-ЯЁ][а-яё]+$', v):
            raise ValueError('Должно содержать только кириллицу и начинаться с заглавной буквы')
        return v

    # Валидатор для номера телефона
    @validator('phone')
    def validate_phone(cls, v):
        if not re.fullmatch(r'^\+7\d{10}$', v):
            raise ValueError('Номер телефона должен быть в формате +7XXXXXXXXXX')
        return v

# Модель для задания 2*
class AppealWithReason(AppealBase):
    reason: Reason

# Модель для задания 3**
class AppealWithMultipleReasons(AppealBase):
    reasons: List[Reason]

@app.post("/appeal/", response_model=AppealBase)
async def create_appeal(appeal: AppealBase):
    save_appeal(appeal.dict())
    return appeal

@app.post("/appeal-with-reason/", response_model=AppealWithReason)
async def create_appeal_with_reason(appeal: AppealWithReason):
    save_appeal(appeal.dict())
    return appeal

@app.post("/appeal-with-multiple-reasons/", response_model=AppealWithMultipleReasons)
async def create_appeal_with_multiple_reasons(appeal: AppealWithMultipleReasons):
    save_appeal(appeal.dict())
    return appeal

def save_appeal(appeal_data: dict):
    appeals.append(appeal_data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(appeals, f, ensure_ascii=False, indent=2, default=str)

@app.get("/appeals/")
async def get_appeals():
    return appeals