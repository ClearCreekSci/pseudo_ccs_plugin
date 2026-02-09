"""
    pseudo.py
    CCS datalogger plugin to simulate different sensors based on configuration 

    Copyright (C) 2026 Clear Creek Scientific

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details. 

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import os
import ccs_base
import random
import datetime
import xml.etree.ElementTree as et

NAME = 'pseudo'

TAG_MAX   = 'max'
TAG_MIN   = 'min'
TAG_UUID  = 'uuid'
TAG_VALUE = 'value'

PHOTO_SUFFIX = '.jpg'

class Value(object):

    def __init__(self):
        self.uuid = None
        self.min = None
        self.max = None


class Pseudo(object):

    def __init__(self):
        self.log_callback = None
        self.values = list()
  
    def get_value(self,vmin,vmax):
        count = 0
        mid = vmin + (vmax - vmin)/2
        rv = random.random() 
        while rv < vmin or rv > vmax:
            count += 1
            v = mid * random.uniform(0.0,1.0)
            if rv < vmin:
                rv += v
            elif rv > vmin:
                rv -= v
            else:
                break
            if count > 100:
                break;
        return rv

    def logmsg(self,msg):
        if None is not self.log_callback:
            self.log_callback(NAME,msg)

    # The following functions implement the interface for a sensor plugin module
    def get_label(self):
        return NAME 

    def get_description(self):
        rv = ''
        for v in self.values:
            rv += ccs_base.labels[v.uuid] + ', '
        return rv 

    def get_uuids(self):
        rv = ()
        for v in self.values:
            rv += (v.uuid,)
        return rv

    # Returns a tuple of tuples, each containing the uuid of the value 
    # and the value itself expressed as a string representing a floating point number
    def get_current_values(self):
        rv = tuple()
        for v in self.values:
            if v.uuid == ccs_base.CCS_PHOTOGRAPH_UUID:
                ts = datetime.datetime.now(datetime.UTC)
                path = '/opt/DataLogger/photos'
                name = ts.strftime('%Y%m%d%I%M%S') + PHOTO_SUFFIX
                full_path = os.path.join(path,name)
                rv += ((v.uuid,full_path),)
            else:
                x = self.get_value(v.min,v.max)
                rv += ((v.uuid,x),)
        return rv 

    def set_config(self,xml):
        self.values = list()
        try:
            root = et.fromstring(xml)
            for node in root.findall(TAG_VALUE):
                uuid_node = node.find(TAG_UUID)
                if None is not uuid_node:
                    new_value = Value()
                    new_value.uuid = uuid_node.text.strip()
                    min_node = node.find(TAG_MIN)
                    if None is not min_node:
                        new_value.min = float(min_node.text.strip())
                    else:
                        new_value.min = 0.0
                    max_node = node.find(TAG_MAX)
                    if None is not max_node:
                        new_value.max = float(max_node.text.strip())
                    else:
                        new_value.max = 100.0
                    self.values.append(new_value)
                else:
                    self.logmsg('Config value has no uuid')
        except Exception as ex:
            self.logmsg('Error parsing config: ' + str(ex))

    def set_log_callback(self,callback):
        self.log_callback = callback


def load():
    return Pseudo()


