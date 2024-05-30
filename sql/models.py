from sqlalchemy import Boolean, Column, DateTime, String, func

from sql.database import Base


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
