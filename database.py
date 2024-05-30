#from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
#from sqlalchemy.orm import DeclarativeBase, sessionmaker
import datetime
import maillogclass
from sqlalchemy import  create_engine, Column, Integer, String, select, update, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base, session, sessionmaker
import const
from maillogclass import MailLogClassInfo

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "12363123"
DB_NAME = "logmaildb"

#DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#engine = create_async_engine(DATABASE_URL)

#async_session_marker = sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)

#class Base(DeclarativeBase):
#    pass

engine = create_engine("postgresql://postgres:12363123@localhost:5432/tes")
print(engine)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# создание объекта Session
session = Session()
# создание конфигурации класса Session
#Session = sessionmaker(bind=some_engine)

# создание объекта Session
session = Session()


class User(Base):
    __tablename__ = "user2"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Message(Base):
    __tablename__ = 'message'
    created = Column(DateTime,nullable=False, server_default=func.now())
    id = Column(String, primary_key=True)
    int_id = Column(String(16), nullable=False)
    str = Column(String, nullable=False)
    status = Column(Boolean)


class Log(Base):
    __tablename__ = 'log'
    created = Column(DateTime,nullable=False, server_default=func.now())
    int_id = Column(String(16), nullable=False)
    str = Column(String, nullable=False)
    address = Column(String, nullable=False, primary_key=True)



# UPDATE name by id
def addUser(id: int, name: str):
    session.add(User(id=id, name=name))  # поиск и обновление значений
    session.commit()


def addintoMessage(created: datetime, id: str, int_id: str, str_log: str, status: bool):
    session.add(Message(
            created = created, id = id, int_id = int_id, str = str_log, status = status))  # поиск и обновление значений
    session.commit()


def addintoLog(created: datetime, int_id: str, str_log: str, address: str):
    session.add(Log(
            created = created,  int_id = int_id, str = str_log, address = address))  # поиск и обновление значений
    session.commit()


def brand_new_iterator():

    for i in range (100000000000000):
        yield i

def set_values_from_mail_log(list_of_mail_log : [MailLogClassInfo] ):
    i_itr = brand_new_iterator()
    for value in list_of_mail_log:
        if value.flag == '=>':
            date_string = value.date + " " + value.time
            format = '%Y-%m-%d %H:%M:%S'
            datetime.datetime.strptime(date_string, format)
            addintoMessage(created=datetime.datetime.now(), id=str(next(i_itr)), int_id=value.id_self,
                           str_log=value.another_information[0], status=False)


if __name__ == '__main__':
    #Base.metadata.drop_all(engine)  # удаление таблиц
    #Base.metadata.create_all(engine)  # создание таблиц
    #addUser(id=2, name="new_name2")
    #addintoMessage(created=datetime.datetime.now(), id='123132', int_id='223344', str_log='1111', status=False)
    addintoLog(created=datetime.datetime.now(), int_id='223344', str_log='1111', address = '1123344')