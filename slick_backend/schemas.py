from typing import Optional
from pydantic import BaseModel

# First we create a BaseModel class 
# So that we can access the attributes of the model. 
# These are our database schemas and dictates how 
# our API will work. 

# We start off with the BaseModel and create a Base class
# this is data that every model will inherit. 

# schemas will be the form that data is returned 

class ContactBase(BaseModel):
    name: str 
    address: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None

# First we define what data a Contact needs to know in order 
# to properly create it. Thankfully, everything within 
# The base class contains all the data needed to make a Contact.
# We don't provide an Id or userId as the Id will be returned, and the 
# userId will be parsed from the href, 
# /user/{id}/contact 
class ContactCreate(ContactBase): 
    pass 

# Next we need to define what kind of data will come back 
# When we read. We want to include the id of contact 
# and the owner's id of the contact when we return. 
class Contact(ContactBase):
    id: int
    owner_id: str

    class Config:
        orm_mode = True
        exclude_unset = True

# For an update
class ContactUpdate(ContactBase):
    # We now make the name field optional as you don't need to actually supply it. 
    # Our URL will always contain the contact_id so we're covered there
    name: Optional[str] = None 

# When we want to delete 
class ContactDelete(ContactBase): 
    pass


# It is left as an exercise to the reader to figure out 
# Why the members are used as they are within the following 
# User classes. 
class UserBase(BaseModel):
    username: str

# Note, when we create, we need to supply the password
class UserCreate(UserBase):
    pass

# However, when we return a user from the API we don't include 
# the pword, only the user ID and the contacts list. 
class User(UserBase):
    id: int
    attempt: list[Contact] = []

    class Config:
        orm_mode = True
        exclude_unset = True

# Response models we'll use for issuing tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True
        exclude_unset = True

class Letters(BaseModel): 
    grey: Optional[str] = None 
    green: Optional[str] = None 
    yellow: Optional[str] = None 
    class Config:
        orm_mode = True
        exclude_unset = True
class AttemptResponse(BaseModel): 
    letter: str 
    state: str 
    class Config:
        orm_mode = True
        exclude_unset = True

class Game(BaseModel): 
    letters: Letters = None
    attempts = list[AttemptResponse] = []
    class Config:
        orm_mode = True
        exclude_unset = True


class TokenData(BaseModel):
    username: str | None = None