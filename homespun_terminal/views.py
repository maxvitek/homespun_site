import datetime

import pandas as pd
from sqlalchemy import func, distinct

from django.shortcuts import render
from models import WemoTimeSeries, HueTimeSeries, NestTimeSeries, ApexTimeSeries, RoombaTimeSeries
from models import session
from services import Flower

def home(request):

    session.commit()

    filter_date = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
    
    wemo_device_count = session.query(func.count(distinct(WemoTimeSeries.device_name))).first()[0]
    wemo = session.query(WemoTimeSeries).order_by(WemoTimeSeries.datetime.desc()).limit(wemo_device_count).all()

    hue_device_count = session.query(func.count(distinct(HueTimeSeries.device_name))).first()[0]
    hue = session.query(HueTimeSeries).order_by(HueTimeSeries.datetime.desc()).limit(hue_device_count).all()

    nest = session.query(NestTimeSeries).order_by(NestTimeSeries.datetime.desc()).limit(1).first()

    apex = session.query(ApexTimeSeries).filter(ApexTimeSeries.value != None).filter(ApexTimeSeries.datetime>filter_date).all()
   
    roomba_device_count = session.query(func.count(distinct(RoombaTimeSeries.device_name))).first()[0]
    roomba = session.query(RoombaTimeSeries).order_by(RoombaTimeSeries.datetime.desc()).limit(roomba_device_count).all()
    
    f = Flower()
    flower = f.get_data(.001)[-1]
    
    return render(request, template_name='home.html', dictionary={'wemo': wemo, 
                                                                  'hue': hue, 
                                                                  'nest': nest,
                                                                  'apex': apex,
                                                                  'roomba': roomba,
                                                                  'flower': flower,
                                                                 })


def chart(request, device=None, chart_type=None):
    if not device:
        raise NoDeviceSpecified()
    if not chart_type:
        raise NoChartTypeSpecified()
    
    filter_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
 
    if device == 'nest':
        nest = session.query(NestTimeSeries).filter(NestTimeSeries.datetime>filter_date).all()
        df = pd.DataFrame([{'datetime': n.datetime, 'value': getattr(n, chart_type)} for n in nest]).set_index('datetime')['value'].dropna()
    elif device == 'apex':
        apex = session.query(ApexTimeSeries).filter(ApexTimeSeries.device_name==chart_type).filter(ApexTimeSeries.datetime>filter_date).all()
        df = pd.DataFrame([{'datetime': a.datetime, 'value': a.value} for a in apex]).set_index('datetime')['value'].dropna()
    elif device == 'wemo':
        wemo = session.query(WemoTimeSeries).filter(WemoTimeSeries.device_name==chart_type).filter(WemoTimeSeries.datetime>filter_date).all()
        df = pd.DataFrame([{'datetime': w.datetime, 'value': float(w.state)} for w in wemo]).set_index('datetime')['value'].dropna()
    elif device == 'hue':
        hue = session.query(HueTimeSeries).filter(HueTimeSeries.device_name==chart_type).filter(HueTimeSeries.datetime>filter_date).all()
        df = pd.DataFrame([{'datetime': h.datetime, 'value': float(h.state) * float(h.reachable)} for h in hue]).set_index('datetime')['value'].dropna()
    elif device == 'roomba':
        roomba = session.query(RoombaTimeSeries).filter(RoombaTimeSeries.device_name==chart_type).filter(RoombaTimeSeries.datetime>filter_date).all()
        df = pd.DataFrame([{'datetime': r.datetime, 'value': r.current} for r in roomba]).set_index('datetime')['value'].dropna()
    elif device == 'flower':
        f = Flower()
        df = pd.DataFrame(f.get_data(1)).set_index('datetime')[chart_type].dropna()

    return render(request, template_name='chart.html', dictionary={'chart_type': 'device' + '_' + chart_type, 'series': df})


class NoChartTypeSpecified(Exception):
    pass


class NoDeviceSpecified(Exception):
    pass
