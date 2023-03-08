from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud
from crud import acta as crud_acta

from schemas.acta import Acta

router = APIRouter()


@router.get("/acta/list", response_model=list[Acta])
async def recuperar_lista_actas(db: Session = Depends(crud.get_db)):
    actas = crud_acta.get_convocatorias(db)
    if not actas:
        raise HTTPException(
            status_code=404,
            detail="No se ha podido recuperar la lista de actas o esta vacia.",
        )
    return actas


@router.get("/acta/edit/{id_acta}", response_model=Acta)
async def recuperar_acta_id(id_acta: str, db: Session = Depends(crud.get_db)):
    return crud_acta.get_convocatoria_id(id_acta, db)


@router.put("/acta/create", response_model=Acta)
async def create_acta(acta_nueva: Acta, db: Session = Depends(crud.get_db)):
    return crud_acta.create_acta(db, acta_nueva)
