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
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile,File

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


class PersonBase(BaseModel):
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


class Person(PersonBase):
    password: str = Field(...,min_length=8)

    #card : str = PaymentCardNumber()

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Debbie Johan",
    #             "last_name": "Arredondo Arteaga",
    #             "age": "31",
    #             "hair_color": "black",
    #             "is_married": False,
    #             "email": "chevi6@gmail.com"
    #         }
    #     }
    

class PersonOut(PersonBase):
    pass
    

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="debbie2022"
        )

@app.get(
        path = "/",
        status_code=status.HTTP_200_OK
        )
def home():
    return {"hello":"world"}

# request and response body

@app.post(
        path = "/person/new",
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED,
        tags=["persons"],
        summary="Create Person in the app"
        )
def create_person(person: Person = Body(...)):
    """
    Create person 

    This path operation creates a person in the app and save the information in the database
    
    Parameters:
    - Request Body parameter:
        - **person: Person** -> A person model with first name, last name, age hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status 
    """
    return person

#validaciones: query parameters

@app.get(
        path="/person/detail",
        status_code=status.HTTP_200_OK,
        tags=["persons"],
        summary="given a Name and Age"
        )
def show_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1, 
        max_length=50,
        title = "Person Name",
        description="This is the person name, it's between 1 and 50 characters",
        example= "Rocio"
        ),
    age: str = Query(
        ...,
        title = "Person age",
        description = "This is the person Age, It's required",
        example=25
        )
):
    """
    Show a person 

    Parameters:
    - Query parameters
        - an optional name
        - an age that it's required 

    Returns the name and the age 
    """
    return {name: age}

#validaciones: path parameters
persons = [1,2,3,4,5]

@app.get(
        path="/person/detail/{person_id}",
        status_code=status.HTTP_200_OK,
        tags=["persons"],
        summary="Get the person based in an ID"
        )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
        )
):
    """
    Show a person 

    this path operation returns a person if it exist in a list 

    Parameters
        - an **person_id** that it must to be greater than cero 

    returns the confirmation of existence 
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this person doesn't exist"
        )
    return {person_id: "It exists!"}

#validaciones: Request Body

@app.put(
        path="/person/{person_id}",
        status_code=status.HTTP_202_ACCEPTED,
        tags=["persons"]
        )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

# forms 

@app.post(
    path = "/login",
    response_model = LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["persons"]
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    return LoginOut(username=username)

# Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["forms"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# files 
@app.post(
    path="/post-image",
    tags=["forms"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }