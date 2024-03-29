from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import crud
from crud import login as crud_login
from crud import usuario as crud_usuario
from schemas.usuario import UsuarioBase, UsuarioDB

router = APIRouter(prefix="/usuario", tags=["Usuario"])


@router.get("/actual", response_model=UsuarioBase)
async def recuperar_usuario_actual(
    current_user: UsuarioBase = Depends(crud_login.get_current_active_user),
) -> UsuarioBase:
    return current_user


@router.get("/list", response_model=List[UsuarioDB])
async def recuperar_list_usuarios(
    db: Session = Depends(crud.get_db),
):
    return crud_usuario.get_users(db)


@router.get("/details/{idUsuario}", response_model=UsuarioDB)
async def get_usuario_id(
    idUsuario: int, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    return crud_usuario.get_user_id(db, idUsuario)


@router.get("/details/{username}", response_model=UsuarioBase)
async def get_usuario_username(
    username: str, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    return crud_usuario.get_user_username(db, username)


@router.post("/create", response_model=UsuarioBase)
async def create_usuario(
    usuario_nuevo: UsuarioBase, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    """
    Create an User with all the information:

    - **nombre**: El nombre
    - **apellidos**: Los apellidos del usuario
    - **username**: El username con el que iniciara sesion.
    - **rol**: El rol del usuario
    - **estado**: El estado del usuario.
    \f
    :param usuario_nuevo: User input.
    """
    return crud_usuario.create_usuario(db, usuario_nuevo)


@router.put("/update", response_model=UsuarioBase)
async def update_usuario(
    usuario_editado: UsuarioDB, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    """
    Update an User with all the information:

    - **idUsuario**: El id del usuario
    - **nombre**: El nombre
    - **apellidos**: Los apellidos del usuario
    - **username**: El username con el que iniciara sesion.
    - **rol**: El rol del usuario
    - **estado**: El estado del usuario.
    \f
    :param usuario_nuevo: User input.
    """
    return crud_usuario.update_usuario(db, usuario_editado)


@router.patch("/disable", response_model=UsuarioBase)
async def desactivar_usuario(
    idUsuario: int, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    return crud_usuario.desactivar_usuario(db, idUsuario)


@router.patch("/enable", response_model=UsuarioBase)
async def activar_usuario(
    idUsuario: int, db: Session = Depends(crud.get_db)
) -> UsuarioDB:
    return crud_usuario.activar_usuario(db, idUsuario)
