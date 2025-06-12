from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Usuario, UsuarioResponse
from utils.connection_db import get_session

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/all", response_model=List[UsuarioResponse])
async def get_all_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Usuario))
    usuarios = result.scalars().all()
    return [UsuarioResponse.model_validate(a) for a in usuarios]

@router.post("/", response_model=UsuarioResponse)
async def crear_usuario(
    nombre: str = Form(...),
    usuario_id: str = Form(...),
    mascotas: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    usuario = Usuario(
        nombre=nombre,
        usuario_id=usuario_id,
        mascotas=mascotas
    )
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario
@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Usuario).where(Usuario.eliminado == False))
    usuarios = result.scalars().all()
    return [UsuarioResponse.model_validate(a) for a in usuarios]

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario_por_id(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario or usuario.eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.model_validate(usuario)

    usuario = await session.get(Usuario, usuario_id)
    if not usuario or usuario.eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = nombre
    usuario.usuario_id = usuario_id
    usuario.mascotas = mascotas
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return UsuarioResponse.model_validate(usuario)

@router.patch("/{usuario_id}", response_model=UsuarioResponse)
async def patch_usuario(
        usuario_id: int,
        data: dict = None,
        session: AsyncSession = Depends(get_session)
    ):
        usuario = await session.get(Usuario, usuario_id)
        if not usuario or usuario.eliminado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if data:
            for key, value in data.items():
                if hasattr(usuario, key) and key not in ("id"):
                    setattr(usuario, key, value)
        await session.commit()
        await session.refresh(usuario)
        return UsuarioResponse.model_validate(usuario)

@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario or usuario.eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.eliminado = True
    await session.commit()
    return {"ok": True}
