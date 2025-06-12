from typing import Optional
from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    mascotas: list["Mascotas"] = Field(default_factory=list)


class Mascotas(SQLModel, table=True):
    mascota_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    vuelo: str
    dueño: "Usuarios" = Field(default_factory="Usuarios")


class Vuelos(SQLModel, table=True):
    vuelo_id: Optional[int] = Field(default=None, primary_key=True)
    origen: str
    destino: str
    viaje: list["Mascotas"] = Field(default_factory=list)

class UsuarioResponse(SQLModel):
    usuario_id: int
    nombre: str
    mascotas: Mascotas

class MascotaResponse(SQLModel):
    mascota_id: int
    nombre: str
    raza: str
    vuelo: Vuelos
    dueño= Usuario

class VueloResponse(SQLModel):
    vuelo_id: int
    origen: str
    destino: str
    viaje: Mascotas
