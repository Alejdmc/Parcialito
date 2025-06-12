from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Usuario, Vuelo, Mascota, MascotaResponse
from utils.connection_db import get_session

router = APIRouter(prefix="/mascotas", tags=["mascotas"])

@router.get("/all", response_model=List[MascotaResponse])
async def get_all_mascotas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Mascota))
    mascotas = result.scalars().all()
    return [MascotaResponse.model_validate(a) for a in mascotas]

@router.post("/", response_model=MascotaResponse)
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
@router.get("/", response_model=List[MascotaResponse])
async def get_mascotas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Mascota).where(Mascota.eliminado == False))
    mascotas = result.scalars().all()
    return [MascotaResponse.model_validate(a) for a in mascotas]

@router.get("/{mascota_id}", response_model=MascotaResponse)
async def get_usuario_por_id(mascota_id: int, session: AsyncSession = Depends(get_session)):
    mascota = await session.get(Mascota, mascota_id)
    if not mascota or Mascota.eliminado:
        raise HTTPException(status_code=404, detail="Mascota no encontrado")
    return MascotaResponse.model_validate(mascota)

    mascota = await session.get(Mascota, mascota_id)
    if not mascota or mascota.eliminado:
        raise HTTPException(status_code=404, detail="mascota no encontrado")
    mascota.nombre = nombre
    mascota.raza = raza
    mascota.vuelo = vuelo
    mascota.mascota_id = mascota_id
    mascota.eliminado = False
    mascota.dueño= dueño
    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    return UsuarioResponse.model_validate(mascota)

@router.patch("/{mascota_id}", response_model=MascotaResponse)
async def patch_mascota(
        mascota_id: int,
        data: dict = None,
        session: AsyncSession = Depends(get_session)
    ):
        mascota = await session.get(Mascota, mascota_id)
        if not mascota or mascota.eliminado:
            raise HTTPException(status_code=404, detail="mascota no encontrado")
        if data:
            for key, value in data.items():
                if hasattr(mascota, key) and key not in ("id"):
                    setattr(mascota, key, value)
        await session.commit()
        await session.refresh(mascota)
        return MascotaResponse.model_validate(mascota)

@router.delete("/{mascota_id}")
async def delete_mascota(mascota_id: int, session: AsyncSession = Depends(get_session)):
    mascota = await session.get(Mascota, mascota_id)
    if not mascota or mascota.eliminado:
        raise HTTPException(status_code=404, detail="Mascota no encontrado")
    mascota.eliminado = True
    await session.commit()
    return {"ok": True}

