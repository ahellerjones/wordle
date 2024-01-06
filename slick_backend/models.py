from sqlalchemy import create_engine, ForeignKey, Column, Integer, String 

engine = create_engine('sqlite:///sql_app.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship

# These are our data models which dictate how 
# data will be organized in our databases.
class user(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)

class daily_attempts(Base): 
    __tablename__ = "daily_attempts"

    # unique ID for each attempt in table
    attempt_id = Column(Integer, primary_key=True, index=True) 
    # references user table, max 6 in this table (since it's a daily table)
    user_id = Column(Integer, ForeignKey('users.user_id') )
    wordle_word = Column(String, ForeignKey('historical_wordles.wordle_word') )
    attempt = Column(String)
    # 1 - 6 based on which attempt
    attempt_number = Column(Integer)

class historical_wordles(Base):
    __tablename__ = "historical_wordles"

    # date + wordle_word = wordle_id; unique and used as dimension
    wordle_id = Column(String, primary_key=True, index=True)
    date = Column(date, unique=True)
    wordle_word = Column(String, primary_key=True)
    # below are statistics related to all past wordle words
    first_attempt_successes = Column(Integer)
    second_attempt_successes = Column(Integer)
    third_attempt_successes = Column(Integer)
    fourth_attempt_successes = Column(Integer)
    fifth_attempt_successes = Column(Integer)


