#python
from typing import Optional

#pydantic
from pydantic import BaseModel

#fastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#models

class Person(BaseModel):
    first_name : str
    last_name : str
    age : int
    hair_color : Optional[str] = None
    is_married : Optional[bool] = None



@app.get("/")
def home():
    return {"hello":"world"}

# request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#validaciones: query parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1, 
        max_length=50,
        title = "Person Name",
        description="This is the person name, it's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title = "Person age",
        description = "This is the person Age, It's required"
        )
):
    return {name: age}

#validaciones: path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0
        )
):
    return {person_id: "It exists!"}