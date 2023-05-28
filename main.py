#python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import PaymentCardNumber 

#fastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#models
class HairColor(Enum):
    white = "white"
    Brown = "brown"
    Black = "black"
    Blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    class Config:
        schema_extra = {
            "example": {
                "city": "Pereira",
                "state": "Risaralda",
                "country": "Colombia",
            }
        }


class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age : int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color : Optional[HairColor] = Field(default=None)
    is_married : Optional[bool] = Field(default=None)
    email : EmailStr = Field(...)
    #card : str = PaymentCardNumber()
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Debbie Johan",
                "last_name": "Arredondo Arteaga",
                "age": "31",
                "hair_color": "black",
                "is_married": False,
                "email": "chevi6@gmail.com"
            }
        }
    



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

#validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results