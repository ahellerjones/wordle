from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import models
import schemas

# MODELS ARE HOW THE DATA IS ORGANIZED IN THE DBs
# SCHEMAS ARE THE DATA THAT COMES IN OR OUT 
# These functions transform data schemas into db models and place them into the dbs.
# Each crud operation function gets
# an instance of the db,
# Special parameters which are parsed from the href
# And the schema which the data comes in on. Ez. 
# And then the methods return the created db object.
# Which actually seems kind of fucked up but oh well. I like 'database schemas' but yolo

def create_user(db: Session, user: schemas.UserCreate): 
    db_user_obj = models.User(username=user.username, 
    hashed_password=user.password)
    db.add(db_user_obj)
    db.commit()
    db.refresh(db_user_obj) # I think this updates the user's ID etc. 
    return db_user_obj
    
def read_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def read_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def read_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: str): 
    db_contact_obj = models.Contact(**contact.dict(), owner_id=user_id) # Unfurl the contact into a dict and put it into a Contact model
    exists = db.query(models.Contact).filter(
        models.Contact.owner_id == user_id
        ).filter(
        models.Contact.name == contact.name
        ).first()
    if exists is not None:
        raise HTTPException(status_code=409, detail="Contact with this ID already exists")
    db.add(db_contact_obj)
    db.commit()
    db.refresh(db_contact_obj)
    return db_contact_obj

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user_id: str): 
    db_contact = db.query(models.Contact).filter(
        models.Contact.owner_id == user_id
        ).filter(
        models.Contact.id == contact_id
        ).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact_data = contact.dict(exclude_unset=True)
    if contact_data.get("name") is not None: 
        # If we're trying to change the name we need to ensure that the name we're
        # going to isn't already in the db.
        does_this_contact_name_exist = db.query(models.Contact).filter(
            models.Contact.owner_id == user_id
            ).filter(
            models.Contact.name == contact_data.get("name")
            ).first()
        # However if someone provides an update with the SAME name to the existing
        # we should not throw an error
        if does_this_contact_name_exist: 
            if does_this_contact_name_exist.id != contact_id:
                raise HTTPException(status_code=409, detail="Contact with this name already exists")

    for key, value in contact_data.items():
        setattr(db_contact, key, value)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def read_contacts_for_user(db: Session, user_id: str): 
    # I think this is how we do this. 
    return db.query(models.Contact).filter(models.Contact.owner_id == user_id)

# Delete contact from database
def delete_contact(db: Session, user_id: str, contact_id: int):
    contact = db.query(models.Contact).filter(
        models.Contact.owner_id == user_id
    ).filter(
        models.Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
        return contact
    else:
        raise HTTPException(status_code=404, detail="Contact not found")
