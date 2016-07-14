from sqlalchemy import create_engine,Column,Integer,String,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///web.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    name = Column(String,primary_key=True)
    passwd = Column(String)
    lastdate = Column(DateTime)

class ProjectName(Base):
    __tablename__ = 'Projnames'

    name = Column(String,primary_key=True)
    url = Column(String )
    introduce = Column(String)
    status = Column(Boolean)
    expiredate = Column(DateTime)

if __name__ == '__main__':
    Base.metadata.create_all(engine)