import crud
import schemas
from fastapi import APIRouter, Depends, HTTPException
import utils 
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()

@router.post("/users/me/contacts/", response_model=schemas.Contact)
def post_contact_for_user(
    user: Annotated[schemas.User, Depends(utils.get_current_user)], 
    contact: schemas.ContactCreate,
    db: Session = Depends(utils.get_db)): 

    return crud.create_contact(db, contact=contact, user_id=user.username)

@router.get("/users/me/contacts/", response_model=list[schemas.Contact])
def read_contacts_for_user(user: Annotated[schemas.User, Depends(utils.get_current_user)], db: Session = Depends(utils.get_db)): 
    contacts = crud.read_contacts_for_user(db, user.username)
    if contacts.count() == 0: 
        return []
    else: 
        return contacts.all()

@router.put("/users/me/contacts/{contact_id}/")
def update_contact_for_user(
    contact_id: int,
    user: Annotated[schemas.User, Depends(utils.get_current_user)], 
    contact_create: schemas.ContactUpdate,
    db: Session = Depends(utils.get_db)): 

    return crud.update_contact(db=db, contact_id=contact_id, contact=contact_create, user_id=user.username)
@router.delete("/users/me/contacts/{contact_id}/")
def update_contact_for_user(
    contact_id: int,
    #contact_delete: schemas.ContactDelete, We could put this in in the future, 
    # but don't really need it for now. 
    user: Annotated[schemas.User, Depends(utils.get_current_user)], 
    db: Session = Depends(utils.get_db)): 

    return crud.delete_contact(db=db, contact_id=contact_id, user_id=user.username)

