from fastapi import FastAPI 
import os, sys
# Fix our stupid fucking path 
# You need to run "uvicorn slick_backend.main:app --host 0.0.0.0 --port 80"
# from the top level project dir. 
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from slick_backend.endpoints import contacts, login


app = FastAPI()
app.include_router(contacts.router)
app.include_router(login.router)

#app.mount("/", StaticFiles(directory="sexy_frontend/dist", html=True), name="dist")


