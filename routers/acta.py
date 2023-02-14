from fastapi import APIRouter
from typing import get_args
from constants import IDIOMAS_DISPONIBLES, fake_actas_DB,  TIPOS_ACTA

router = APIRouter()


@router.get("/acta/correct/{id}")
async def recuperar_acta(id: str):
    return fake_actas_DB[1]


@router.get("/acta/list")
async def recuperar_actas():
    actas = []
    actas = fake_actas_DB
    return actas


@router.get("/acta/idiomas")
async def recuperar_idiomas_disponibles():
    return get_args(IDIOMAS_DISPONIBLES)


@router.get("/acta/tipos")
async def recuperar_tipos_acta():
    return get_args(TIPOS_ACTA)


@router.get("/acta/tipos")
async def recuperar_horarios_acta():
    return get_args(TIPOS_ACTA)
