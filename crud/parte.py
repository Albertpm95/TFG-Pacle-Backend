import json
from textwrap import indent

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud import tarea as crud_tarea
from models.parte import Parte, ParteCorregida
from schemas.parte import ParteBase, ParteBaseDB


def create_parte(parte: ParteBase, db: Session):
    tareas = crud_tarea.create_tareas(parte.tareas, db)
    parte_db = Parte(
        puntuacionMaxima=parte.puntuacionMaxima,
        tipo=parte.tipo,
        tareas=tareas
    )
    db.add(parte_db)
    db.flush()
    db.refresh(parte_db)

    return parte_db

async def create_parte_corregida(parte: ParteCorregida, db: Session):
    async with db.begin():
        existe_parte = get_parte_id(parte.parte.idParte, db)
        parte_db = ParteCorregida(
            idParte=parte.idParte,
            puntuacionMaxima=parte.parte.puntuacionMaxima,
            parte=existe_parte,
            correccion=parte.correccion,
            observaciones=parte.observaciones
        )
        db.add(parte_db)
        await db.flush()
        db.refresh(parte_db)
        print(json.dumps(jsonable_encoder(parte_db)))
    return parte_db


def update_parte(parte: ParteBaseDB, db:Session):
    existe_parte: Parte = get_parte_id(idParte=parte.idParte, db=db)
    if not existe_parte:
        raise HTTPException(
            status_code=404, detail=f"No existe la parte de {parte.tipo}, no puede actualizarse."
        )
    existe_parte.puntuacionMaxima=parte.puntuacionMaxima
    existe_parte.tareas=crud_tarea.create_tareas(parte.tareas, db)
    print(json.dumps(jsonable_encoder(parte)))
    print(json.dumps(jsonable_encoder(parte.puntuacionMaxima)))
    print(json.dumps(jsonable_encoder(existe_parte)))
    db.commit()
    db.refresh(existe_parte)
    print(json.dumps(jsonable_encoder(existe_parte)))
    return existe_parte
        
def get_parte_id(idParte: int, db: Session):
    return db.query(Parte).filter(Parte.idParte == idParte).first()

def delete_parte(db: Session, idParte: int):
    existe_parte: Parte = get_parte_id(db, idParte)
    if not existe_parte:
        raise HTTPException(
            status_code=404, detail="No existe ese genero, no puede borrarse."
        )
    db.delete(existe_parte)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se puede borrar la parte porque esta siendo referenciada en algun sitio.")

    return {"Borrado": "Borrada el parte."}