from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud import alumno as crud_alumno
from crud import convocatoria as crud_convocatoria
from crud import parte as crud_parte
from models.acta import Acta
from schemas.acta import ActaBase

""" CRUD Principal """


def create_acta(db: Session, acta: ActaBase):
    existe_convocatoria = crud_convocatoria.get_convocatoria_id(db=db, idConvocatoria=acta.convocatoria.idConvocatoria)
    if not existe_convocatoria:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no existe la convocatoria.",
        )

    existe_alumno = crud_alumno.get_alumno_id(acta.alumno.idAlumno, db=db)
    if not existe_alumno:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no existe el alumno.",
        )
    parte_expresion_oral = crud_parte.create_parte_corregida(acta.expresionEscrita, db=db)
    if not parte_expresion_oral:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no se ha podido crear la parte de expresion oral.",
        )
    parte_expresion_escrita = crud_parte.create_parte_corregida(acta.expresionOral, db=db)
    if not parte_expresion_escrita:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no se ha podido crear la parte de expresion escrita.",
        )
    parte_comprension_auditiva = crud_parte.create_parte_corregida(acta.comprensionAuditiva, db=db)
    if not parte_comprension_auditiva:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no se ha podido crear la parte de comprension auditiva.",
        )
    parte_comprension_lectora = crud_parte.create_parte_corregida(acta.comprensionLectora, db=db)
    if not parte_comprension_lectora:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido crear el acta, no se ha podido crear la parte de comprension lectora.",
        )
    acta_db = Acta(
        alumno=existe_alumno,
        comprensionAuditiva=parte_comprension_auditiva,
        comprensionLectora=parte_comprension_lectora,
        expresionEscrita=parte_expresion_escrita,
        expresionOral=parte_expresion_oral,
        convocatoria=existe_convocatoria,
        fecha=acta.fecha,
        resultado=acta.resultado
        )
    db.add(acta_db)
    db.commit()
    db.refresh(acta_db)
    return acta_db

def get_actas(db: Session):
    return db.query(Acta).all()


def get_acta_id(idActa: int, db: Session):
    return db.query(Acta).filter(Acta.idActa == idActa).first()


def existe_acta_alumno_acta(idActa: int, idAlumno: int, db: Session):
    return db.query(Acta).filter(Acta.idActa == idActa, Acta.idAlumno == idAlumno).first()


def delete_acta(db: Session, idActa: int):
    existe_acta: Acta = get_acta_id()(db, idActa)
    if not existe_acta:
        raise HTTPException(status_code=404, detail="No existe ese genero, no puede borrarse.")
    db.delete(existe_acta)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Cannot delete row due to foreign key constraint.")

    return {"Borrado": "Borrada el acta."}
