from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from routes.vuelos import router as ruta_vuelos
from routes.usuarios import router as ruta_usuarios
from routes.mascotas import router as ruta_mascotas


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(ruta_mascotas)
app.include_router(ruta_vuelos)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(ruta_usuarios)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
