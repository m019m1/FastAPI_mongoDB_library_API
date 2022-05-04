from fastapi import APIRouter, HTTPException, Path, Query, Body
from schemas import Author
from models import Authors
from fastapi.encoders import jsonable_encoder
from mongoengine import *
from paginate import paginate
import json

router = APIRouter()
PREFIX_AUTHORS = '/authors'


@router.post('', status_code=201)
def create_author(author: Author = Body(..., description="Enter author's full name")):
    try:
        new_author = Authors(**jsonable_encoder(author))
        new_author.save()
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    return {
        "success": True,
        "detail": json.loads(new_author.to_json())
    }


@router.get('')
def get_authors(full_name: str = Query('', description="Search by full name"),
                page_size: int = Query(
                    5, description="Quantity of results per page"),
                page_num: int = Query(1, description="Page number")):
    params = locals()
    try:
        authors = Authors.objects(full_name__icontains=full_name)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    return paginate(authors, params, PREFIX_AUTHORS)


@router.get('/{pk}')
def get_single_author(pk: str = Path(..., max_length=24, description="Author's primary key")):
    try:
        author = Authors.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    if not author:
        raise HTTPException(status_code=422, detail="Author doesn't exist")

    return json.loads(author.to_json())


@router.patch('/{pk}')
def modify_author(
        pk: str = Path(..., max_length=24, description="Author's primary key"),
        full_name: str = Body('', embed=True, min_length=1, max_length=70, description="New author's full name")):
    try:
        author = Authors.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    if not author:
        raise HTTPException(status_code=422, detail="Author doesn't exist")

    author.full_name = full_name
    try:
        author.save()
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    return {
        "success": True,
        "detail": json.loads(author.to_json())
    }


@router.delete('/{pk}')
def delete_author(pk: str = Path(..., max_length=24, description="Author's primary key")):
    try:
        author = Authors.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    if not author:
        raise HTTPException(status_code=422, detail="Author doesn't exist")

    try:
        author.delete()
    except OperationError:
        raise HTTPException(
            status_code=422, detail="Operation denied. Delete all books of this author first")
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    return {
        "success": True,
        "detail": "Author has been deleted"
    }
