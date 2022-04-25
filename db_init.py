import asyncio, json
from mongoengine import connect
from fastapi.encoders import jsonable_encoder  
from models import Authors, Editions, Books
from routes.authors import create_author
from routes.editions import create_edition
from schemas import Book
  
connect(db='library', host='localhost', port=27017)

with open('db_sample/authors.json') as f:
    authors = json.load(f)
with open('db_sample/editions.json') as f:
    editions = json.load(f)
with open('db_sample/books.json') as f:
    books = json.load(f)

def create_book(book: Book):
    authors = Authors.objects(full_name__in = book['authors'])
    edition = Editions.objects(name = book['edition']).first()
    new_book = Books(**jsonable_encoder(book))
    new_book.authors = authors
    new_book.edition = edition
    new_book.save()

if __name__ == "__main__":
    for author in authors:
        asyncio.run(create_author({
            'full_name': author
        }))
    for edition in editions:
        asyncio.run(create_edition({
            'name': edition
        }))
    for book in books:
        create_book(book)
    