from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:12363@localhost:5432/ParseMailBase")
Base = declarative_base()
Session = sessionmaker(bind=engine)
