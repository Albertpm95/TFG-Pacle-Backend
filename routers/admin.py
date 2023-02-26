from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

import csv
import codecs

from crud import crud
from crud import usuario as crud_usuario
from schemas.usuario import UsuarioBase, UsuarioCreacion, UsuarioLogin, UsuarioOptional

router = APIRouter()


@router.get("/admin/usuarios/list", response_model=list[UsuarioBase])
async def recuperar_list_usuarios(db: Session = Depends(crud.get_db)):
    return crud_usuario.get_users(db)


@router.post("/admin/upload")
async def cargar_excel(excel: UploadFile):
    numero_de_alumnos_cargados = 0
    csvReader = csv.DictReader(codecs.iterdecode(excel.file, "utf-8"))
    data = {}
    for rows in csvReader:
        key = rows["DNI"]
        data[key] = rows
    return numero_de_alumnos_cargados


@router.get("/admin/usuario/{id_usuario}")
async def get_usuario_id(id_usuario: str, db: Session = Depends(crud.get_db)):
    return crud_usuario.get_user_id(db, id_usuario)


@router.get("/admin/usuario/{username}")
async def get_usuario_username(username: str, db: Session = Depends(crud.get_db)):
    return crud_usuario.get_user_username(db, username)


@router.post("/admin/usuario/alta")
async def alta_usuario(usuario: UsuarioCreacion, db: Session = Depends(crud.get_db)):
    return crud_usuario.alta_usuario(db, usuario)


@router.patch("/admin/usuario/desactivar")
async def desactivar_usuario(id_usuario: str, db: Session = Depends(crud.get_db)):
    return crud_usuario.desactivar_usuario(db, id_usuario)


@router.patch("/admin/usuario/activar")
async def activar_usuario(id_usuario: str, db: Session = Depends(crud.get_db)):
    return crud_usuario.activar_usuario(db, id_usuario)


@router.patch("/admin/usuario/update", response_model=UsuarioBase)
async def update_usuario(
    id_usuario, usuario_updated: UsuarioOptional, db: Session = Depends(crud.get_db)
):
    return crud_usuario.update_usuario(db, id_usuario, usuario_updated)
