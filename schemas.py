from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Author(BaseModel):
    full_name: str = Field(min_length=1, max_length=70, description="Author's name must be at most 70 characters")

class Edition(BaseModel):
    name: str = Field(min_length=1, max_length=70, description="Edition name must be at most 70 characters")
    
class Book(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Book title must be at most 200 characters")
    authors: List[str] = Field(min_length=1, description="Book must have at least 1 author")
    edition: str = Field(min_length=1, description="Book must have exactly 1 edition")
    year: int = Field(
        ge=1450, 
        le=datetime.now().year, 
        description="Book publishing year must be between 1450 and current")
        