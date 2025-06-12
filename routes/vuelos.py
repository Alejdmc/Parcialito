from fastapi import APIRouter, Form, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Vuelo, VueloResponse
from utils.connection_db import get_session

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

@router.get("/all", response_model=List[VueloResponse])
async def get_all_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Vuelo))
    vuelo = result.scalars().all()
    return [VueloResponse.model_validate(a) for a in vuelo]

@router.post("/", response_model=VueloResponse)
async def crear_vuelo(
    origen: str = Form(...),
    mascotas: str = Form(...),
    vuelo_id: str = Form(...),
    destino: str = Form(...),
    fecha_salida: str = Form(...),
    fecha_llegada: str = Form(...),
    activo: str = Form("true"),
    session: AsyncSession = Depends(get_session)
):
    vuelo = Vuelo(
        origen=origen,
        destino=destino,
        fecha_salida=fecha_salida,
        fecha_llegada=fecha_llegada,
        vuelo_id=vuelo_id,
        mascotas=mascotas,
        activo=activo
    )
    session.add(vuelo)
    await session.commit()
    await session.refresh(vuelo)
    return vuelo
    @router.get("/", response_model=List[VueloResponse])
    async def get_vuelo(session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(Vuelo).where(Vuelo.eliminado == False))
        vuelo = result.scalars().all()
        return [VueloResponse.model_validate(a) for a in vuelo]
    @router.get("/{vuelo_id}", response_model=VueloResponse)
    async def get_vuelo_por_id(vuelo_id: int, session: AsyncSession = Depends(get_session)):
        try:
            stmt = select(Vuelo).where(Vuelo.id == vuelo_id)
            result = await session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener vuelo: {str(e)}")
        return VueloResponse.model_validate(vuelo)

@router.delete("/{vuelo_id}")
async def delete_vuelo(vuelo_id: int, session: AsyncSession = Depends(get_session)):
    vuelo = await session.get(Vuelo, vuelo_id)
    if not vuelo or vuelo.eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    vuelo.eliminado = True
    await session.commit()
    return {"ok": True}



