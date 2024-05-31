from sqlalchemy import Boolean, Column, DateTime, String, func

from sql.database import Base

#структура для таблицы Message
class Message(Base):
    """
        структура для таблицы message
    """
    __tablename__ = "message"
    created = Column(DateTime, nullable=False, server_default=func.now())
    id = Column(String, primary_key=True)
    int_id = Column(String(16), nullable=False)
    str = Column(String, nullable=False)
    status = Column(Boolean)


#структура для таблицы Base
class Log(Base):
    """
    структура для таблицы log
    т.к. sqlalchemy предполагает обязательное наличие PrimaryKey,
    объявлен фальшивый primary_key, в объявлении таблицы его нет -
    запросы будут работать корректно
    """
    __tablename__ = "log"
    created = Column(
        DateTime, nullable=False, server_default=func.now(), primary_key=True
    )
    int_id = Column(String(16))
    str = Column(String)
    address = Column(String)
