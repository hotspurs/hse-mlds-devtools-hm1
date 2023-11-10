import random
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


@app.get('/')
def root():
    return "string"


@app.get('/post', response_model=list[Timestamp], summary='Get Posts')
def post():
    return post_db


@app.post('/post', response_model=Timestamp, summary='Create Post')
def post():
    last_post = post_db[-1]
    new_post = Timestamp(id=last_post.id + 1, timestamp=last_post.timestamp + 1)
    post_db.append(new_post)
    return new_post


@app.get('/dog', response_model=list[Dog], summary='Get Dogs')
def dogs(kind: DogType = None):
    return filter(lambda dog: True if kind is None else kind == dog.kind, list(dogs_db.values()))


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    existing_dog = dogs_db.get(dog.pk)

    if existing_dog is not None:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')

    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}', response_model=Dog | None, summary='Get Dog By Pk')
def create_dog(pk: int):
    dog = dogs_db.get(pk)
    if dog is not None:
        return dog
    else:
        raise HTTPException(status_code=404,
                            detail='Not found PK.')


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def patch_dog(pk: int, dog: Dog):
    old_dog = dogs_db.get(pk)
    if old_dog is not None:
        dogs_db[pk] = dog
        return dog
    else:
        raise HTTPException(status_code=404,
                            detail='Not found PK.')
