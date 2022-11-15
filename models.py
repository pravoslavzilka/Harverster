from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, Date, DateTime, Float, PickleType
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base


class User(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(128))
    permission = Column(Integer)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.name


class Coordinator(Base):
    __tablename__ = "coordinators"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    phone = Column(String(20))
    password = Column(String(128))

    hubs = relationship("Hub", back_populates="coordinator")

    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Coordinator %r>' % self.name


class Hub(Base):
    __tablename__ = "hubs"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    district = Column(String(120))
    city = Column(String(120))
    address = Column(String(120))
    contact_person_name = Column(String(120))
    idp = Column(Integer)
    last_idp_update = Column(DateTime)
    orders = relationship("Order", back_populates="hub")
    coordinator_id = Column(Integer, ForeignKey('coordinators.id'))

    coordinator = relationship("Coordinator", back_populates="hubs", foreign_keys=[coordinator_id])

    def __init__(self, name):
        self.name = name


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    measurement_unit = Column(String(15))
    quantity = Column(Float)

    def __init__(self, name):
        self.name = name


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    status = Column(Integer)
    content = Column(PickleType)
    hub_id = Column(Integer, ForeignKey('hubs.id'))

    hub = relationship("Hub", back_populates="orders", foreign_keys=[hub_id])


