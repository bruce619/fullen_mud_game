# Ref https://docs.sqlalchemy.org/en/14/orm/quickstart.html#declare-models
# Ref https://alembic.sqlalchemy.org/en/latest/autogenerate.html#codecell3 using alembic to create tables
# command: alembic init migration
# command: alembic revision --autogenerate -m "Create db models"
# command: alembic upgrade heads

from sqlite3 import Connection
from sqlalchemy.engine import Engine
from sqlalchemy import event
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Table, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, false, true, text

# this is the base class for class definitions
Base = declarative_base()


# configuring sqlite to enforce foreignkey constraint
# this is because by default fk constraints have no effect on the operation of the table.
# REF: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#codecell3
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class Race(Base):
    # __tablename__ represents the name of the table in the db

    __tablename__ = 'race'
    """
        ORM ata class for the different races
        1. Orixinais
        2. Viaxeiros 
    """

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(12), nullable=True)
    description = Column(String(200), nullable=True)
    users = relationship("User", lazy='subquery', back_populates="race")

    def __str__(self):
        return f'A character of the race {self.name}: {self.description}'


# setting up Many#To#Many relation relationship
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many#many-to-many

user_orb = Table('user_orb',
                 Base.metadata,
                 Column('user_id', Integer, ForeignKey('user.id')),
                 Column('orb_id', Integer, ForeignKey('orb.id')),
                 Column('created_at', DateTime, default=datetime.now, server_default=func.now())
                 )

user_inventory = Table('user_inventory',
                       Base.metadata,
                       Column('user_id', Integer, ForeignKey('user.id')),
                       Column('inventory_id', Integer, ForeignKey('inventory.id')),
                       Column('created_at', DateTime, default=datetime.now, server_default=func.now())
                       )

user_weapon = Table('user_weapon',
                    Base.metadata,
                    Column('user_id', Integer, ForeignKey('user.id')),
                    Column('weapon_id', Integer, ForeignKey('weapon.id')),
                    Column('created_at', DateTime, default=datetime.now, server_default=func.now())
                    )


location_orbs = Table('location_orbs',
                      Base.metadata,
                      Column('location_id', Integer, ForeignKey('location.id')),
                      Column('orb_id', Integer, ForeignKey('orb.id'), nullable=True),
                      )

user_location = Table('user_location',
                      Base.metadata,
                      Column('user_id', Integer, ForeignKey('user.id')),
                      Column('location_id', Integer, ForeignKey('location.id'), nullable=True),
                      Column('created_at', DateTime, default=datetime.now, server_default=func.now())
                      )


class User(Base):
    __tablename__ = 'user'

    """
        The user class represents the gamers
        username password and email are stored here 
    """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)  # the users username has to be unique
    password = Column(String(16), nullable=False)
    strength_level = Column(Integer, default=10, server_default='10')
    won = Column(Boolean, default=False, server_default=false())
    rank = Column(String(35), default='baixo', server_default='baixo')  # needed
    coins = Column(Integer, default=10, server_default='10')  # needed
    lost = Column(Integer, default=0, server_default='0')
    # one to many
    race_id = Column(Integer, ForeignKey("race.id", ondelete="SET NULL"), nullable=False)
    race = relationship("Race", lazy='subquery', back_populates="users")
    # many to many
    weapons = relationship("Weapon", lazy='subquery', secondary="user_weapon", back_populates="users")
    inventories = relationship("Inventory", lazy='subquery', secondary="user_inventory", back_populates="users")
    locations = relationship("Location", lazy='subquery', secondary="user_location", back_populates="users")
    orbs = relationship("Orb", lazy='subquery', secondary="user_orb", back_populates="users")
    # date created
    created_date = Column(DateTime, default=datetime.now, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_onupdate=text('CURRENT_TIMESTAMP'), server_default=text('CURRENT_TIMESTAMP'))


class Weapon(Base):
    __tablename__ = 'weapon'

    """
        This table stores the weapons
    """

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(30), nullable=True)
    price = Column(Integer, default=0, server_default='0')
    users = relationship("User", lazy='subquery', secondary="user_weapon", back_populates="weapons")


class Inventory(Base):
    __tablename__ = 'inventory'
    """
     This contains all the users inventories like clothes, weapons, potions 
    """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(30), nullable=True)
    description = Column(String(200), nullable=True)
    price = Column(Integer, default=0, server_default='0')
    users = relationship("User", lazy='subquery', secondary="user_inventory", back_populates="inventories")


class Realm(Base):
    __tablename__ = 'realm'

    """
        Represents the Parent Location where cahracter are located in 
        1. Inferno
        2. Terra
        3. Paraíso. # this represents the fina realm 
    """

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(12), nullable=True)
    description = Column(String(200), nullable=True)
    locations = relationship("Location", lazy='subquery', back_populates='realm')


class Location(Base):
    __tablename__ = 'location'

    """
        This represents the locations within a realm.
        It has a reference to the realm table
        cascade means delete when parent is deleted
    """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(30), nullable=True)
    description = Column(String(200), nullable=True)
    # one to many
    realm_id = Column(Integer, ForeignKey("realm.id", ondelete="CASCADE"), nullable=False)
    realm = relationship("Realm", lazy='subquery', back_populates='locations')
    # many to many
    users = relationship("User", lazy='subquery', secondary="user_location", back_populates="locations")
    orbs = relationship("Orb", lazy='subquery', secondary="location_orbs", back_populates='locations')
    # relationship with monster
    monsters = relationship("Monster", lazy='subquery', back_populates='locations')


class Monster(Base):
    __tablename__ = 'monster'
    """
        This represents the monsters players will be against
        Different monsters are usually in certain locations of the game world
    """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(30), nullable=True)
    description = Column(String(200), nullable=True)
    power_level = Column(Integer, default=0, server_default='0', nullable=True)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=True)
    locations = relationship("Location", lazy='subquery', back_populates='monsters')


class Orb(Base):
    __tablename__ = 'orb'

    """
        This class represents the orbs the users have to acquire in the game
        1. Poder
        2. Coñecemento
        3. vida
    """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(12), nullable=True)
    description = Column(String(200), nullable=True)
    users = relationship("User", lazy='subquery', secondary="user_orb", back_populates="orbs")
    locations = relationship("Location", lazy='subquery', secondary="location_orbs", back_populates='orbs')

    def __repr__(self):
        return f'OrbModel(id={self.id}, name={self.name}, description={self.description}'






