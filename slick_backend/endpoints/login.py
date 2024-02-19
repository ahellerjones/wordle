import crud
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import utils 
import schemas
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from datetime import datetime, timedelta
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi import Cookie, FastAPI
import string, random
from fastapi import Request



router = APIRouter()
# Here we use a fastAPI shortcut in the Annotated, we really are just creating a OAuth2Password.. object and putting it 
# into the form_data object. 
# This endpoint also ONLY WORKS for existing users, new users should post to 
# `/signup`. We issue tokens here. 

# Here the user GETs on `/token`, we issue them a token to be used as a Cookie
@router.post("/", response_model=schemas.Game)
def landing_page(request: Request): 
    if request.cookies.get('user-cookie') is not None: 
        # Need to return an inprogress here game
        attempts = crud.read_game(request.cookies.get('user-cookie'))
        if attempts is not None:
        for attempt in attempts: 

        resp = schemas.Game()
        #return Response(content=request.cookies.get('user-cookie'))
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": id_generator()}, expires_delta=access_token_expires
    )
    response = Response()
    response.set_cookie(key="user-cookie", value=access_token)
    return response



@router.get("/token") 
async def get_tocken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(utils.get_db)):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# This just simply signs up a user, they will need to login afterwards
# This doesn't give back an access token unf. It might be able to but idk. 
@router.post("/signup")
async def signup(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    db_user = crud.read_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=401, detail="Username already exists")

    # Replace the passed user password with a hashed version
    # Then stick it in the db.
    user.password = utils.get_password_hash(user.password)
    return crud.create_user(db=db,user=user)

# @router.get("/users/me")
# async def read_users_me(current_user: Annotated[schemas.User, Depends(utils.get_current_user)]):
#     return current_user