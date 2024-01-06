from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Here's how we're actually going to do it. 
'''
We use the ORM pattern, object relational mapping 
We create a class which represents a table in a SQL database.
Each attribute gets a column. 
'''
# This is the path to our db, I believe that the path is ./rolodex.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a database session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Our base class (??) which we'll inherit from 
Base = declarative_base()
