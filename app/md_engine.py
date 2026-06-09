from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(
    DATABASE_URI,
    echo=True
)

Session = sessionmaker(bind=engine)
session=Session()
