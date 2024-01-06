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
    """
    Create a new user record in the database.

    Parameters:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        user: The newly created user record.
            user_id (str): The ID of the user.
    """
    new_user_record = models.user(user_id=user)
    db.add(new_user_record)
    db.commit()
    db.refresh(new_user_record)
    return new_user_record


def read_game(db: Session, user_id: str):
    """
    Retrieve the daily attempts of a user from the database.

    Parameters:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        Query: The query result containing the daily attempts of the user (max 6)
            attempt contains (user_id, attempt, attempt_number)
    """
    attempts = db.query(models.daily_attempts)\
        .filter(models.daily_attempts.user_id == user_id)\
        .order_by(models.daily_attempts.attempt_number.asc())

    if not attempts:
        raise HTTPException(status_code=404, detail="No game found for user. User needs an attempt.")

    return attempts

def create_attempt(db: Session, user_id: str, attempt: str):
    """
    Creates a new attempt record in the database for a given user.

    Parameters:
        db (Session): The database session object.
        user_id (str): The identifier of the user for whom the attempt is being created.
        attempt (str): The attempt string.

    Returns:
    - The newly created attempt record (user_id, attempt, attempt_number)
    """

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
    todays_record = db.query(models.historical_wordles)\
        .filter(models.historical_wordles.date == date)

    if not todays_record:
        new_date_record = models.historical_wordles(date=date, wordle_word=wordle_word, \
            first_attempt_successes = 1 if attempt_number == 1 else 0, \
            second_attempt_successes = 1 if attempt_number == 2 else 0, \
            third_attempt_successes = 1 if attempt_number == 3 else 0, \
            fourth_attempt_successes = 1 if attempt_number == 4 else 0, \
            fifth_attempt_successes = 1 if attempt_number == 5 else 0
            )
    else:
        
            


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