from sqlalchemy import create_engine, ForeignKey, Column, Integer, String 

engine = create_engine('sqlite:///sql_app.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship


# These are our data models which dictate how 
# data will be organized in our databases.
class User(Base):
    # Tells SQLAlchemy the table to use
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    enabled = bool
    contacts = relationship("Contact", back_populates="owner")
    # This is what relates a user to contacts,
    # Each user will contain a list of contacts


class Contact (Base): 
    __tablename__ = "contacts"
    # While both id and name are enforced to be unique, we include id
    # so that it can easily be referenced within urls and contain the 
    # same body request as the Create.
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True) # What does index do?
    address = Column(String,index=True)
    phoneNumber = Column(String,index=True)
    email = Column(String,index=True)
    birthday = Column(String,index=True)
    owner_id = Column(String,ForeignKey('users.username') )
    owner = relationship('User', back_populates='contacts')



