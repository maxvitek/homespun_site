import datetime

import pandas as pd
from sqlalchemy import func, distinct

from django.shortcuts import render
from models import WemoTimeSeries, HueTimeSeries, NestTimeSeries, ApexTimeSeries
from models import session

def home(request):

    session.commit()

    filter_date = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
    
    wemo_device_count = session.query(func.count(distinct(WemoTimeSeries.device_name))).first()[0]
    wemo = session.query(WemoTimeSeries).order_by(WemoTimeSeries.datetime.desc()).limit(wemo_device_count).all()
    print wemo

    hue_device_count = session.query(func.count(distinct(HueTimeSeries.device_name))).first()[0]
    hue = session.query(HueTimeSeries).order_by(HueTimeSeries.datetime.desc()).limit(hue_device_count).all()

    nest = session.query(NestTimeSeries).order_by(NestTimeSeries.datetime.desc()).limit(1).first()

    apex = session.query(ApexTimeSeries).filter(ApexTimeSeries.value != None).filter(ApexTimeSeries.datetime>filter_date).all()
    
    return render(request, template_name='home.html', dictionary={'wemo': wemo, 
                                                                  'hue': hue, 
                                                                  'nest': nest,
                                                                  'apex': apex,
                                                                  })
