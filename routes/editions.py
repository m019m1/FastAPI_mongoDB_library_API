from fastapi import APIRouter, HTTPException, Path, Query, Body
from schemas import Edition
from models import Editions
from fastapi.encoders import jsonable_encoder
from mongoengine import *
from paginate import paginate
import json

router = APIRouter()
PREFIX_EDITIONS = '/editions'

@router.post('', status_code=201)
async def create_edition(edition: Edition):
    try:
        new_edition = Editions(**jsonable_encoder(edition))
        new_edition.save()
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")
    return {
            "success": True,
            "detail": json.loads(new_edition.to_json())
        }

@router.get('')
async def get_editions(name: str = Query('', description="Search by name"), 
                       page_size: int = Query(5, description="Quantity of results per page"), 
                       page_num: int = Query(1, description="Page number")):
    params = locals()
    try:
        editions = Editions.objects(name__icontains = name)
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")
    return paginate(editions, params, PREFIX_EDITIONS)


@router.get('/{pk}')
async def get_single_edition(pk: str = Path(..., max_length=24)):
    try:
        edition = Editions.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail= err.message)
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")

    if not edition:
        raise HTTPException(status_code=422, detail="Edition doesn't exist")
        
    return json.loads(edition.to_json())

@router.patch('/{pk}')
async def modify_edition(
    pk: str = Path(..., max_length=24, description="Edition primary key"),
    name: str = Body('', embed=True, min_length=1, max_length=70, description="New edition name")):
    try:
        edition = Editions.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail= err.message)
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")
    if not edition:
        raise HTTPException(status_code=422, detail="Edition doesn't exist")

    edition.name = name
    try:
        edition.save()
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")
        
    return {
        "success": True,
        "detail": json.loads(edition.to_json())
    }

@router.delete('/{pk}')
async def delete_edition(pk: str = Path(..., max_length=24, description="Edition primary key")):
    try:
        edition = Editions.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail= err.message)
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")
    if not edition:
        raise HTTPException(status_code=422, detail="Edition doesn't exist")

    try:
        edition.delete()
    except OperationError:
        raise HTTPException(status_code=422, detail= "Operation denied. Delete all books of this edition first")
    except Exception:
        raise HTTPException(status_code=503, detail= "Something went wrong")

    return {
        "success": True,
        "detail": "Edition has been deleted"
    }
