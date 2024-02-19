from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import models
import schemas
import datetime.datetime

# MODELS ARE HOW THE DATA IS ORGANIZED IN THE DBs
# SCHEMAS ARE THE DATA THAT COMES IN OR OUT 

# These functions transform data schemas into db models and place them into the dbs.
# Each crud operation function gets
# an instance of the db,
# Special parameters which are parsed from the href
# And the schema which the data comes in on. Ez. 
# And then the methods return the created db object.
# Which actually seems kind of fucked up but oh well. I like 'database schemas' but yolo

def create_user(db: Session, user_id: str): 
    new_user_record = models.user(user_id=user)
    db.add(new_user_record)
    db.commit()
    db.refresh(new_user_record)
    return new_user_record


def read_game(db: Session, user_id: str):
    attempts = db.query(models.daily_attempts)\
        .filter(models.daily_attempts.user_id == user_id)\
        .order_by(models.daily_attempts.attempt_number.asc())
    # This should return an empty list, it's very possible to read a game with no attempts in it. 
    if not attempts:
        raise HTTPException(status_code=404, detail="No game found for user. User needs an attempt.")

    return attempts

def create_attempt(db: Session, user_id: str, attempt: str):

    last_attempt_number = db.query(models.daily_attempts)\
        .filter(models.daily_attempts.user_id == user_id)\
        .order_by(models.daily_attempts.attempt_number.desc())\
        .first().attempt_number

    attempt_record = models.daily_attempts(user_id=user_id, attempt=attempt, \
            attempt_number=1 if not last_attempt_number else last_attempt_number+1)

    db.add(attempt_record)
    db.commit()
    db.refresh(attempt_record) 
    return attempt_record

def update_historical_wordle(db: Session, user_id: str, date: datetime.date, wordle_word: str, attempt_number: int):
    date_record = models.historical_wordles(date=date, wordle_word=wordle_word, \
        attempt_number=attempt_number)


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