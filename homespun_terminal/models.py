import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Boolean, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import homespun_site.settings as settings

e = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=e)
session = Session()

Base = declarative_base()


class WemoTimeSeries(Base):
    '''
    Collects a time series of observations of Wemo devices
    '''
    __tablename__ = 'wemo'
    
    datetime = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    device_name = Column(String(50), primary_key=True)
    state = Column(Boolean)

    def __repr__(self):
        return '<Wemo(%s::%s::%s)>' % (self.datetime, self.device_name, str(self.state))


class HueTimeSeries(Base):
    '''
    Collects a time series of observations of Hue devices
    '''
    __tablename__ = 'hue'
    datetime = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    device_name = Column(String(50), primary_key=True) 
    alert = Column(String(25))
    brightness = Column(Integer)
    colormode = Column(String(10))
    effect = Column(String(25))
    hue = Column(Integer)
    state = Column(Boolean)
    reachable = Column(Boolean)
    saturation = Column(Integer)
    x = Column(Float)
    y = Column(Float)

    def __repr__(self):
        return '<Hue(%s::%s::%s::)>' % (self.datetime, self.device_name, str(self.state))


class NestTimeSeries(Base):
    '''
    Collects nest data
    '''
    __tablename__ = 'nest'
    datetime = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)

    def __repr__(self):
        return '<Nest(%s::%s::%s::)>' % (self.datetime, str(self.temperature), str(self.humidity))


class ApexTimeSeries(Base):
    '''
    apex aquacontroller
    '''
    __tablename__ = 'apex'
    datetime = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    device_name = Column(String(50), primary_key=True)
    state = Column(Boolean, nullable=True)
    value = Column(Float, nullable=True)

    def __repr__(self):
        if self.state:
            metric = self.state
        else:
            metric = self.value
        return '<Apex(%s::%s::%s)>' % (self.datetime, self.device_name, str(metric))


class RoombaTimeSeries(Base):
    '''
    roombas!
    '''
    __tablename__ = 'roomba'
    datetime = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    device_name = Column(String(50), primary_key=True)
    remote_opcode = Column(Integer)
    buttons = Column(Integer)
    distance = Column(Float)
    angle = Column(Float)
    current = Column(Float)
    change = Column(Float)
    capacity = Column(Float)

    def __repr__(self):
        return '<Roomba(%s::%s::%s)>' % (self.datetime, self.device_name, self.remote_opcode)
