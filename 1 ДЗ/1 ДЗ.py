from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import re
import operator

app = FastAPI()


class SimpleOperation(BaseModel):
    a: float
    op: str
    b: float


class ExpressionRequest(BaseModel):
    expression: str


# Глобальная переменная для хранения текущего выражения
current_expression = ""


@app.post("/calculate/simple")
async def calculate_simple(operation: SimpleOperation):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    if operation.op not in ops:
        return {"error": "Unsupported operation"}

    try:
        result = ops[operation.op](operation.a, operation.b)
        return {"result": result}
    except ZeroDivisionError:
        return {"error": "Division by zero"}


@app.post("/expression/set")
async def set_expression(expr: ExpressionRequest):
    global current_expression
    # Проверка выражения на допустимые символы
    if not re.match(r'^[0-9+\-*/(). ]+$', expr.expression):
        return {"error": "Invalid characters in expression"}

    current_expression = expr.expression
    return {"message": "Expression set successfully", "expression": current_expression}


@app.get("/expression/get")
async def get_expression():
    global current_expression
    return {"current_expression": current_expression}


@app.post("/expression/evaluate")
async def evaluate_expression():
    global current_expression
    if not current_expression:
        return {"error": "No expression set"}

    try:
        # Безопасное вычисление выражения
        result = eval(current_expression, {"__builtins__": None}, {})
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}