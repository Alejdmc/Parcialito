from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Usuario, Vuelo, Mascota
from utils.connection_db import get_session

router = APIRouter(prefix="/usuarios", tags=["usuarios"])