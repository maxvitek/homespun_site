import difflib

from ouimeaux.environment import Environment
from phue import Bridge
from nest import Nest as NestAPI

import homespun_site.settings as settings

class Command(object):
    def __init__(self):
        pass

    def on(self):
        raise OverrideMethod()

    def off(self):
        raise OverrideMethod()


class Wemo(Command):
    def __init__(self):
        self.env = Environment(with_discovery=False, with_subscribers=False)
        self.env.start()

    def on(self, device):
        switch = self.env.get_switch(closest_match(device, self.env.list_switches()))
        switch.basicevent.SetBinaryState(BinaryState=1)

    def off(self, device):
        switch = self.env.get_switch(closest_match(device, self.env.list_switches())) 
        switch.basicevent.SetBinaryState(BinaryState=0)


class Hue(Command):
    def __init__(self):
        self.bridge = Bridge(ip=settings.HUE_IP_ADDRESS, username=settings.HUE_USER)
    
    def on(self, device):
        light = str(closest_match(device, self.bridge.get_light_objects('name').keys()))
        self.bridge.set_light(light, 'on', True)

    def off(self, device):
        light = str(closest_match(device, self.bridge.get_light_objects('name').keys()))
        self.bridge.set_light(light, 'on', False)


class Nest(Command):
    def __init__(self):
        self.nest = NestAPI(settings.NEST_USER, settings.NEST_PASSWD)

    def set(self, temp):
        self.nest.set_target_temperature(int(temp))


def closest_match(string, target_list):
    results = []
    for target in target_list:
        results.append((target, difflib.SequenceMatcher(None, string, target.lower()).ratio()))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results[0][0]


class OverrideMethod(Exception):
    pass
