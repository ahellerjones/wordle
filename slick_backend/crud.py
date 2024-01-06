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

def create_user(db: Session, user_id: String): 
    new_user_obj = models.user(user_id=user)
    db.add(new_user_obj)
    db.commit()
    db.refresh(new_user_obj)
    return new_user_obj


def read_game(db: Session, user_id: String):
    last_record = db.query(models.daily_attempts)\
        .filter(models.daily_attempts.user_id == user_id)\
        .order_by(models.daily_attempts.attempt_number.asc())

    if not last_record:
        # could create user here
        raise HTTPException(status_code=404, detail="No game found for user. User needs an attempt.")

    return last_record

def create_attempt(db: Session, user_id: String, attempt: String):
    attempt_obj = models.Attempt(user_id=user_id, attempt=attempt)

    db.add(attempt_obj)
    db.commit()
    db.refresh(attempt_obj) # I think this updates the user's ID etc. 
    return attempt_obj

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