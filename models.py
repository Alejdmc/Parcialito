from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    mascotas: List["Mascota"] = Relationship(back_populates="usuario")

class Mascota(SQLModel, table=True):
    mascota_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    vuelo_id: Optional[int] = Field(default=None, foreign_key="vuelo.vuelo_id")
    dueño_id: Optional[int] = Field(default=None, foreign_key="usuario.usuario_id")
    dueño: Optional["Usuario"] = Relationship(back_populates="mascotas")
    vuelo: Optional["Vuelo"] = Relationship(back_populates="mascotas")

class Vuelo(SQLModel, table=True):
    vuelo_id: Optional[int] = Field(default=None, primary_key=True)
    origen: str
    destino: str
    viaje: str
    mascotas: List["Mascota"] = Relationship(back_populates="vuelo")
    activo: bool = Field(default=True)

class UsuarioResponse(SQLModel):
    usuario_id: int
    nombre: str
    mascotas: List[str]  # Lista de nombres de mascotas o IDs

class MascotaResponse(SQLModel):
    mascota_id: int
    nombre: str
    raza: str
    vuelo: Optional[str]  # Puedes poner el ID o nombre del vuelo
    dueño: Optional[str]  # Puedes poner el nombre del dueño

class VueloResponse(SQLModel):
    vuelo_id: int
    origen: str
    destino: str
    viaje: str