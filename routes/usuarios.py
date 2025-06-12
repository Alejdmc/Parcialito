from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Usuario, Vuelo, Mascota
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
    pais: str = Form(...),
    genero_principal: str = Form(...),
    activo: str = Form("true"),
    imagen: UploadFile = File(None),
    session: AsyncSession = Depends(get_session)
):
    @router.get("/", response_model=List[UsuarioResponse])
    async def get_usuarios(session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(Usuario).where(Usuario.eliminado == False))
        usuarios = result.scalars().all()
        return [UsuarioResponse.model_validate(a) for a in usuarios]

    @router.get("/{usuario_id}", response_model=UsuarioResponse)
    async def get_usuario_por_id(artista_id: int, session: AsyncSession = Depends(get_session)):
        usuario = await session.get(Usuario, artista_id)
        if not usuario or usuario.eliminado:
            raise HTTPException(status_code=404, detail="Artista no encontrado")
        return UsuarioResponse.model_validate(usuario)