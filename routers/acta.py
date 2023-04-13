from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud
from crud import acta as crud_acta

from schemas.acta import ActaDB, ActaBase

router = APIRouter(prefix="/acta", tags=['Acta'])


@router.get("/list", response_model=list[ActaDB])
async def recuperar_lista_actas(db: Session = Depends(crud.get_db)):
    return crud_acta.get_actas(db)


@router.get("/details/{id_acta}", response_model=ActaDB)
async def recuperar_acta_id(id_acta: int, db: Session = Depends(crud.get_db)):
    return crud_acta.get_acta_id(id_acta, db)


@router.post("/create", response_model=ActaDB)
async def create_acta(acta_nueva: ActaBase, db: Session = Depends(crud.get_db)):
    return crud_acta.create_acta(db, acta_nueva)
