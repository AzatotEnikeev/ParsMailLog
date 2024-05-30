# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    func,
    text,
)
from sqlalchemy.orm import declarative_base, session, sessionmaker

from backend.mail_log_class import MailLogClassInfo

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "12363123"
DB_NAME = "logmaildb"

# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine = create_async_engine(DATABASE_URL)

# async_session_marker = sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)

# class Base(DeclarativeBase):
#    pass

engine = create_engine("postgresql://postgres:12363123@localhost:5432/tes")
print(engine)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# создание объекта Session
session = Session()
# создание конфигурации класса Session
# Session = sessionmaker(bind=some_engine)

# создание объекта Session
session = Session()


class User(Base):
    __tablename__ = "user2"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Message(Base):
    __tablename__ = "message"
    created = Column(DateTime, nullable=False, server_default=func.now())
    id = Column(String, primary_key=True)
    int_id = Column(String(16), nullable=False)
    str = Column(String, nullable=False)
    status = Column(Boolean)


class Log(Base):
    __tablename__ = "log"
    created = Column(
        DateTime, nullable=False, server_default=func.now(), primary_key=True
    )
    int_id = Column(String(16))
    str = Column(String)
    address = Column(String)


# UPDATE name by id
def addUser(id: int, name: str):
    session.add(User(id=id, name=name))  # поиск и обновление значений
    session.commit()


def addintoMessage(created: datetime, id: str, int_id: str, str_log: str, status: bool):
    session.add(
        Message(created=created, id=id, int_id=int_id, str=str_log, status=status)
    )  # поиск и обновление значений
    session.commit()


def addintoLog(created: datetime, int_id: str, str_log: str, address: str):
    session.add(
        Log(created=created, int_id=int_id, str=str_log, address=address)
    )  # поиск и обновление значений
    session.commit()


def brand_new_iterator():

    for i in range(100000000000000):
        yield i


def format_todatetime(date_string, format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(date_string, format)


def set_values_from_mail_log(list_of_mail_log: [MailLogClassInfo]):
    i_itr = brand_new_iterator()
    for value in list_of_mail_log:
        if value.id:
            date_string = format_todatetime(value.date + " " + value.time)
            addintoMessage(
                date_string,
                id=value.id[0],
                int_id=value.id_self,
                str_log=value.another_information,
                status=False,
            )
        else:
            date_string = format_todatetime(value.date + " " + value.time)
            addintoLog(
                created=date_string,
                int_id=value.id_self,
                str_log=value.another_information,
                address=value.mail_adress,
            )


def select_values_from_tables(name_address: str):
    name_address = f"'{name_address}'"
    query = text(
        "select * from (select created, str  from log where log.int_id in"
        " (Select distinct(int_id) from log l where l.address = "
        + name_address
        + ")) t1"
        " union all "
        "select * from (select created, str from message where  message.int_id in (Select distinct(int_id) "
        "from log l where l.address =" + name_address + ") ) t2"
    )
    return session.execute(query)


if __name__ == "__main__":
    result = select_values_from_tables("kuxanwyqalsszn@gmail.com")
    for record in result:
        print("\n", record)
    # Base.metadata.drop_all(engine)  # удаление таблиц
    # Base.metadata.create_all(engine)  # создание таблиц
    # addUser(id=2, name="new_name2")
    # addintoMessage(created=datetime.datetime.now(), id='123132', int_id='223344', str_log='1111', status=False)
