from typing import Optional, List

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select


app = FastAPI(title="API CRUD con FastAPI y SQLModel")


# -----------------------------
# Base de datos
# -----------------------------
DATABASE_URL = "postgresql://fastapidb:Db12345678@fastapidb.cx6qo6ac8m6c.us-east-2.rds.amazonaws.com:5432/fastapi_db"

engine = create_engine(DATABASE_URL, echo=True)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# -----------------------------
# Modelos Usuario
# -----------------------------
class UsuarioBase(SQLModel):
    nombre: str
    correo: str
    edad: int


class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    edad: Optional[int] = None


# -----------------------------
# Modelos Libro
# -----------------------------
class LibroBase(SQLModel):
    titulo: str
    autor: str
    paginas: int
    disponible: bool = True


class Libro(LibroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class LibroCreate(LibroBase):
    pass


class LibroUpdate(SQLModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    paginas: Optional[int] = None
    disponible: Optional[bool] = None


# -----------------------------
# Ruta principal
# -----------------------------
@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}


# ==================================================
# CRUD USUARIOS
# ==================================================

@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate):
    with Session(engine) as session:
        nuevo_usuario = Usuario.model_validate(usuario)
        session.add(nuevo_usuario)
        session.commit()
        session.refresh(nuevo_usuario)
        return nuevo_usuario


@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios():
    with Session(engine) as session:
        usuarios = session.exec(select(Usuario)).all()
        return usuarios


@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario


@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        datos_actualizados = datos.model_dump(exclude_unset=True)
        for key, value in datos_actualizados.items():
            setattr(usuario, key, value)

        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        session.delete(usuario)
        session.commit()
        return {"mensaje": "Usuario eliminado correctamente"}


# ==================================================
# CRUD LIBROS
# ==================================================

@app.post("/libros/", response_model=Libro)
def crear_libro(libro: LibroCreate):
    with Session(engine) as session:
        nuevo_libro = Libro.model_validate(libro)
        session.add(nuevo_libro)
        session.commit()
        session.refresh(nuevo_libro)
        return nuevo_libro


@app.get("/libros/", response_model=List[Libro])
def listar_libros():
    with Session(engine) as session:
        libros = session.exec(select(Libro)).all()
        return libros


@app.get("/libros/{libro_id}", response_model=Libro)
def obtener_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro


@app.put("/libros/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, datos: LibroUpdate):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        datos_actualizados = datos.model_dump(exclude_unset=True)
        for key, value in datos_actualizados.items():
            setattr(libro, key, value)

        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro


@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        session.delete(libro)
        session.commit()
        return {"mensaje": "Libro eliminado correctamente"}
