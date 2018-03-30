#!/bin/python3
from pydbus.generic import signal


class Example(object):
    """
    <node>
        <interface name='com.HACGI.example'>
            //test
            <property name='SomeProperty' type='s' access='readwrite'>
                <annotation
                name='org.freedesktop.DBus.Property.EmitsChangedSignal'
                value='true'/>
            </property>

            <method name='EchoString'>
                <arg type='s' name='a' direction='in'/>
                <arg type='s' name='response' direction='out'/>
            </method>
            <method name='Quit'>
            </method>
        </interface>
    </node>
    """

    def EchoString(self, s):
        """return whatever is passed to it"""
        return s

    def __init__(self):
        self._someProperty = 'initial value'

    @property
    def SomeProperty(self):
        return self._someProperty

    @SomeProperty.setter
    def SomeProperty(self, value):
        self._someProperty = value
        self.PropertiesChanged(
            'com.HACGI.example', {'SomeProperty': self.SomeProperty}, [])

    PropertiesChanged = signal()

    def Quit(self):
        global loop
        loop.quit()


def callback(*data):
    print(data)


from pydbus import SessionBus
bus = SessionBus()
# from base.global_config import BUS_NAME
bus.publish('com.HACGI.example', ('/com/HACGI/example', Example()))
# example = bus.get(BUS_NAME, 'com.HACGI.example')
# example.PropertiesChanged.connect(callback)

from gi.repository import GLib
loop = GLib.MainLoop()
loop.run()
