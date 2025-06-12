from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from routes.vuelos import router as ruta_vuelos
from routes.usuarios import router as ruta_usuarios
from routes.mascotas import router as ruta_mascotas
from routes.mascotas import Mascota,MascotaResponse,Form,  List
from utils.connection_db import init_db, get_session, engine
from pydantic import BaseModel
import models
import os
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(ruta_mascotas)
app.include_router(ruta_vuelos)
app.include_router(ruta_usuarios)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home():
    return {"message": "Hello World"}





@app.get("/mascotas/", response_class=HTMLResponse)
async def info_page(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})
@app.get("/all", response_model=List[MascotaResponse])
async def get_all_mascotas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Mascota))
    mascotas = result.scalars().all()
    return [MascotaResponse.model_validate(a) for a in mascotas]

@app.post("/", response_model=MascotaResponse)
async def crear_mascota(
    nombre: str = Form(...),
    mascota_id: int = Form(...),
    raza: str = Form(...),
    vuelo: str = Form(...),
    dueño: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    mascota = Mascota(
        nombre=nombre,
        mascota_id=mascota_id,
        vuelo=vuelo,
        dueño=dueño,
        raza=raza,

    )
    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    return mascota
