#! /usr/bin python3.11.1

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, AnyStr, Literal
from fastapi import HTTPException
from datetime import datetime
app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', response_model=AnyStr)
def root():
    return 'Hello, buddy'


@app.post('/post', response_model=Timestamp)
def get_post():
    timestamp_record = Timestamp(id=len(post_db), timestamp=int(datetime.now().strftime('%S')))
    post_db.append(timestamp_record)
    return timestamp_record


@app.get('/dog', response_model=List[Dog])
def get_dog(kind: Literal["terrier", "bulldog", "dalmatian", ""]):
    if kind:
        dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return dogs
    else:
        return list(dogs_db.values())


@app.post('/dog', response_model=Dog)
def create_dog(new_dog: Dog):
    if new_dog.pk in [dog.pk for dog in dogs_db.values()]:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    else:
        dogs_db[new_dog.pk] = Dog(name=new_dog.name, pk=new_dog.pk, kind=new_dog.kind)
    return new_dog


@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int):
    if pk not in [dog.pk for dog in dogs_db.values()]:
        raise HTTPException(status_code=422,
                            detail='The specified PK does not exist.')
    return dogs_db[pk]


@app.patch('/dog/{pk}')
def update_dog(pk: int, new_dog: Dog):
    if pk not in [dog.pk for dog in dogs_db.values()]:
        raise HTTPException(status_code=422,
                            detail='The specified PK does not exist.')
    dogs_db[pk] = Dog(name=new_dog.name, pk=pk, kind=new_dog.kind)
    return dogs_db[pk]
