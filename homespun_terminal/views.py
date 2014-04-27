import datetime
import json
import urllib

import pandas as pd
from sqlalchemy import func, distinct

from django.shortcuts import render
from django.http import HttpResponse

from models import WemoTimeSeries, HueTimeSeries, NestTimeSeries, ApexTimeSeries, RoombaTimeSeries
from models import session
from services import Flower
from commands import Wemo as WemoCC
from commands import Hue as HueCC

def home(request):

    session.rollback()
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
    device = urllib.unquote(device)
    chart_type = urllib.unquote(chart_type)

    # print 'device: ', device
    # print 'chart_type: ', chart_type

    session.rollback()
    session.commit()

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


def wemo(request, command=None, device=None):
    if not command:
        raise NoCommandSpecified()
    if device:
        device = urllib.unquote(device)

    if command == 'ls':
        devices = session.query(distinct(WemoTimeSeries.device_name)).all()
        response = '<p>'
        for d in devices:
            response += "'" + d[0] + "'</br>"
        response += '</p>'
    
    elif command == 'on':
        wemo = WemoCC().on(device)
        response = '<p>' + device + ' turned on.</p>'
    
    elif command == 'off':
        wemo = WemoCC().off(device)
        response = '<p>' + device + ' turned off.</p>'

    elif command == 'completion':
        completion = []
        devices = session.query(distinct(WemoTimeSeries.device_name)).all()
        for d in devices:
            completion.append(d.lower().replace(' ', '_'))
        response = json.dumps(completion)

    return HttpResponse(response)


def hue(request, command=None, device=None):
    if not command:
        raise NoCommandSpecified()
    if device:
        device = urllib.unquote(device)

    if command == 'ls':
        devices = session.query(distinct(HueTimeSeries.device_name)).all()
        response = '<p>'
        for d in devices:
            response += "'" + d[0] + "'</br>"
        response += '</p>'

    elif command == 'on':
        hue = HueCC().on(device)
        response = '<p>' + device + ' turned on.</p>'

    elif command == 'off':
        hue = HueCC().off(device)
        response = '<p>' + device + ' turned off.</p>'

    return HttpResponse(response)

class NoChartTypeSpecified(Exception):
    pass


class NoDeviceSpecified(Exception):
    pass


class NoCommandSpecified(Exception):
    pass
