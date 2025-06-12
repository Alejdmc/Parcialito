from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Usuario(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    mascotas: str


class Mascota(SQLModel, table=True):
    mascota_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    vuelo: str
    dueño: str


class Vuelo(SQLModel, table=True):
    vuelo_id: Optional[int] = Field(default=None, primary_key=True)
    origen: str
    destino: str
    viaje: str
    mascotas: list["Mascota"] = Field(default_factory=list)
    activo: bool = Field(default=True)

class UsuarioResponse(SQLModel):
    usuario_id: int
    nombre: str
    mascotas: str

class MascotaResponse(SQLModel):
    mascota_id: int
    nombre: str
    raza: str
    vuelo: str
    dueño= str

class VueloResponse(SQLModel):
    vuelo_id: int
    origen: str
    destino: str
    viaje: str
