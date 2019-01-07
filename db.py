from datetime import datetime
import os

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db_url = os.environ['DATABASE_URL']
# print(db_url)
# engine = sa.create_engine(db_url, echo=True)
engine = sa.create_engine(db_url)
create_session = sessionmaker(bind=engine)
session = create_session()

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    role = sa.Column(sa.String(128), primary_key=True)
    level = sa.Column(sa.Integer, nullable=False)

class User(Base):
    __tablename__ = 'users'
    username = sa.Column(sa.Unicode(128), primary_key=True)
    role = sa.Column(sa.ForeignKey('roles.role'))
    hash = sa.Column(sa.String(256), nullable=False)
    email_addr = sa.Column(sa.String(128))
    desc = sa.Column(sa.String(128))
    creation_date = sa.Column(sa.String(128), nullable=False)
    last_login = sa.Column(sa.String(128), nullable=False)
    entries = relationship('Entry', backref='creator', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Entry(Base):
    __tablename__ = 'entry'
    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.ForeignKey('users.username'))
    pattern = sa.Column(sa.String(500))
    testdata = sa.Column(sa.String(500))
    description = sa.Column(sa.String(100))
    flags = sa.Column(sa.String(5))
    date_added = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):

        return '<Regex {} is {}>'.format(self.id, self.pattern)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
