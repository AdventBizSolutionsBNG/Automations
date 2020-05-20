from collections import namedtuple
from enum import Enum

import json
import os
import sys
import logging


Domains = namedtuple('Domains', ['value'])
LicensingTypes = namedtuple('Domains', ['value'])
Editions = namedtuple('Domains', ['value'])
InstanceTypes = namedtuple('Domains', ['value'])


lstDomains = []
master_file_loc = os.path.append(os.path.curdir,"config","masters.json")

with open(master_file_loc, "r") as f:
    fdata = json.load(f)

class Domains(Enum):
    @property
    def type(self):
        return self.value


class LicensingTypes(Enum):
    @property
    def type(self):
        return self.value


class Editions(Enum):
    @property
    def type(self):
        return self.value


class InstanceTypes(Enum):
    @property
    def type(self):
        return self.value


class Namespace:
    __namespace_name = ""

    def __init__(self):
        try:
            pass
        except Exception as e:
            print('Error in loading Namespace")

