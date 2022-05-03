from fastapi import APIRouter, HTTPException, Path, Query, Body
from schemas import Book
from models import Authors, Editions, Books
from fastapi.encoders import jsonable_encoder
from mongoengine import *
from mongoengine.queryset.visitor import Q
import json
from datetime import datetime
from paginate import paginate

router = APIRouter()
PREFIX_BOOKS = '/books'


@router.post('', status_code=201)
def create_book(book: Book = Body(..., description="Enter valid authors' and edition IDs")):
    authors = []
    try:
        # authors = Authors.objects(id__in = book.authors) - uncaughtable ValidationError! O_o
        for item in book.authors:
            author = Authors.objects.with_id(item)
            if author:
                authors.append(author)
        edition = Editions.objects.with_id(book.edition)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    if len(authors) != len(book.authors):
        raise HTTPException(
            status_code=422, detail="At least one of the authors doesn't exist")
    elif not edition:
        raise HTTPException(status_code=422, detail="Edition doesn't exist")

    try:
        new_book = Books(**jsonable_encoder(book))
        new_book.save()
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    return {
        "success": True,
        "detail": json.loads(new_book.to_json())
    }


@router.get('')
def get_books(
        title: str = Query('', max_length=100, description="Search by title"),
        author: str = Query('', max_length=70,
                            description="Search by author's full name"),
        edition: str = Query(
            '', max_length=70, description="Search by edition name"),
        page_size: int = Query(5, description="Quantity of results per page"),
        page_num: int = Query(1, description="Page number")):
    params = locals()
    try:
        authors = Authors.objects(full_name__icontains=author)
        editions = Editions.objects(name__icontains=edition)
        books = Books.objects(Q(title__icontains=title)
                              & Q(authors__in=authors)
                              & Q(edition__in=editions))
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    return paginate(books, params, PREFIX_BOOKS)


@router.get('/{pk}')
def get_single_book(pk: str = Path(..., max_length=24)):
    try:
        book = Books.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    if not book:
        raise HTTPException(status_code=422, detail="Book doesn't exist")

    return json.loads(book.to_json())


@router.patch('/{pk}')
def modify_book(
        pk: str = Path(..., max_length=24, description="Book primary key"),
        title: str = Body('', embed=True, max_length=200,
                          description="New book title"),
        year: int = Body(None, embed=True, ge=1450, le=datetime.now().year, description="New book publishing year")):

    try:
        book = Books.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    if not book:
        raise HTTPException(status_code=422, detail="Book doesn't exist")
    if title:
        book.title = title
    if year:
        book.year = year
    book.save()
    try:
        book.save()
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    return {
        "success": True,
        "detail": json.loads(book.to_json())
    }


@router.delete('/{pk}')
def delete_book(pk: str = Path(..., max_length=24, description="Book primary key")):
    try:
        book = Books.objects.with_id(pk)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")
    if not book:
        raise HTTPException(status_code=422, detail="Book doesn't exist")

    try:
        book.delete()
    except Exception:
        raise HTTPException(status_code=503, detail="Something went wrong")

    return {
        "success": True,
        "detail": "Book has been deleted"
    }
