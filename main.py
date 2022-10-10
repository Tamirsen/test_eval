from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
from evaluate import tokenize, evaluate
app = FastAPI()


class Eval(BaseModel):
    response: str


class CustomException(Exception):
    pass


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exception: CustomException):
    return JSONResponse(status_code=400, content={"message": "Incorrect input"})


@app.exception_handler(HTTPException)
async def my_exception_handler(request, exception):
    return PlainTextResponse(str(exception.detail), status_code=exception.status_code)


@app.get("/")
@app.get("/index")
async def root():
    return {"message": "Hello World"}


@app.get("/eval", status_code=200)
async def eval_get(phrase: str) -> Eval:
    try:
        ev = await evaluate(tokenize(phrase))
    except Exception:
        raise HTTPException(status_code=400, detail="incorrect input")
    return Eval(response=phrase + '=' + str(ev))


@app.post("/eval", status_code=201)
async def eval_post(phrase: str) -> Eval:
    try:
        ev = await evaluate(tokenize(phrase))
    except Exception:
        raise CustomException
    return Eval(response=phrase + '=' + str(ev))
