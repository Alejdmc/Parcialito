from typing import Optional
from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    mascotas: list["Mascota"] = Field(default_factory=list)


class Mascota(SQLModel, table=True):
    mascota_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    vuelo: str
    dueño: "Usuario" = Field(default_factory="Usuarios")


class Vuelo(SQLModel, table=True):
    vuelo_id: Optional[int] = Field(default=None, primary_key=True)
    origen: str
    destino: str
    viaje: list["Mascota"] = Field(default_factory=list)
    mascotas: list["Mascota"] = Field(default_factory=list)
    activo: bool = Field(default=True)

class UsuarioResponse(SQLModel):
    usuario_id: int
    nombre: str
    mascotas: Mascota

class MascotaResponse(SQLModel):
    mascota_id: int
    nombre: str
    raza: str
    vuelo: Vuelo
    dueño= Usuario

class VueloResponse(SQLModel):
    vuelo_id: int
    origen: str
    destino: str
    viaje: Mascota
