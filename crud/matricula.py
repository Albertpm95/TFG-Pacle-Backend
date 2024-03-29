from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import alumno as crud_alumno
from crud import convocatoria as crud_convocatoria
from models.alumno import Alumno as mod_alumno
from models.convocatoria import Convocatoria as mod_convocatoria
from models.shared import AlumnosConvocatoria
from schemas.alumno import AlumnoDB as sch_alumnoDB
from schemas.convocatoria import ConvocatoriaDB as sch_convocatoriaDB


def get_matriculas(db: Session):
    return db.query(AlumnosConvocatoria).all()


def get_alumno_convocatoria(alumno: mod_alumno, convocatoria: mod_convocatoria, db: Session):
    return db.query(AlumnosConvocatoria).filter(
        AlumnosConvocatoria.alumno.has(idAlumno = alumno.idAlumno),
        AlumnosConvocatoria.convocatoria.has(idConvocatoria = convocatoria.idConvocatoria)
    ).first()

def get_alumnos_by_convocatoria(idConvocatoria: int, db: Session):
    alumnos_convocatoria = db.query(AlumnosConvocatoria).filter(AlumnosConvocatoria.idConvocatoria==idConvocatoria).all()
    alumnos = [ac.alumno for ac in alumnos_convocatoria]
    return alumnos

def matricular_alumno_convocatoria(alumno: sch_alumnoDB, convocatoria: sch_convocatoriaDB, db: Session):
    existe_alumno: mod_alumno = crud_alumno.get_alumno_id(alumno.idAlumno, db=db)
    if not existe_alumno:
        raise HTTPException(
            status_code=404,
            detail="No se encuentra el alumno seleccionada.",
        )
    existe_convocatoria: mod_convocatoria = crud_convocatoria.get_convocatoria_id(convocatoria.idConvocatoria, db)
    if not existe_convocatoria:
        raise HTTPException(
            status_code=404,
            detail="No se encuentra la convocatoria seleccionada.",
        )
    existe_matricula = get_alumno_convocatoria(alumno, convocatoria, db)
    if existe_matricula:
        raise HTTPException(
            status_code=409,
            detail="Ese alumno ya esta matriculado en esa convocatoria.",
        )
    matricula = AlumnosConvocatoria(idConvocatoria=existe_convocatoria.idConvocatoria, idAlumno=existe_alumno.idAlumno, convocatoria=existe_convocatoria, alumno=existe_alumno)
    db.add(matricula)
    try:
        db.commit()
        return True
    except:
        return False
