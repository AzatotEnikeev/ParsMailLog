from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:12363123@localhost:5432/tes")
Base = declarative_base()
Session = sessionmaker(bind=engine)
