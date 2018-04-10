from base.abstract.service_type_interface import ServiceTypeController
from base.abstract.service_interface import ServiceInterface
from base.abstract.type_interface import CT_ABC
from base.utils.configabc import ConfigABC
from access.dbus import sm
import os


class ServiceABC(ServiceInterface, ServiceTypeController, ConfigABC):

    @property
    def dbus(self):
        return """
    <node>
        <interface name='{}.{}'>
            // DBus information
            <property name='BUS_NAME' type='s' access='readwrite'></property>
            <property name='OBJECT_PATH' type='s' access='readwrite'></property>
            // HACGI meta
            <property name='Type' type='s' access='readwrite'></property>
            <property name='ServiceName' type='s' access='readwrite'></property>
            // access modules meta
            <property name='ServiceIsRunning' type='b' access='readwrite' />
            <property name='ServiceAutoStart' type='b' access='readwrite' />
            <method name='Start'></method>
            <method name='Stop'></method>
            // 
            <method name='HasHoldInterface'>
                <arg type='s' name='InterfaceName' direction='in'/>
                <arg type='b' name='ret_has_own' direction='out'/>
            </method>
            <method name='CallControlInterface'>
                <arg type='s' name='InterfaceName' direction='in'/>
                <arg type='s' name='arg_JSON_Value' direction='in'/>
                <arg type='s' name='ret_JSON_Value' direction='out'/>
            </method>
            <method name='getAllInterfaces'>
                <arg type='as' name='allInterfaces' direction='out'/>
            </method>
        </interface>
    </node>
    """.format(self.BUS_NAME, self.ServiceName)

    # dbus bus_name, unique.
    @property
    def BUS_NAME(self):
        if hasattr(self, 'bus_name'):
            return getattr(self, 'bus_name')
        else:
            self.bus_name = self.getKeyFromConfig(
                'BUS_NAME', str, "com.HACGI.access.Service.{}".format(self.ServiceName))
            return self.bus_name

    @BUS_NAME.setter
    def BUS_NAME(self, value):
        self.bus_name = value
        self.setKeyToSaveToConfig('OBJECT_PATH', value)

    # dbus object_path, unique.
    @property
    def OBJECT_PATH(self):
        if hasattr(self, 'object_path'):
            return getattr(self, 'object_path')
        else:
            self.object_path = self.getKeyFromConfig(
                'OBJECT_PATH', str, "/com/HACGI/access/Service/{}".format(self.ServiceName))
            return self.object_path

    @OBJECT_PATH.setter
    def OBJECT_PATH(self, value):
        self.object_path = value
        self.setKeyToSaveToConfig('OBJECT_PATH', value)

    # service_type.
    @property
    def Type(self):
        if hasattr(self, 'type'):
            return getattr(self, 'type')
        else:
            self.type = self.getKeyFromConfig(
                'Type', str, "unknown")
            return self.type

    @Type.setter
    def Type(self, value):
        self.type = value
        self.setKeyToSaveToConfig('Type', value)

    # service_name.
    @property
    def ServiceName(self):
        if hasattr(self, 'service_name'):
            return getattr(self, 'service_name')
        else:
            self.service_name = self.getKeyFromConfig(
                'ServiceName', str, "unknown")
            return self.service_name

    @ServiceName.setter
    def ServiceName(self, value):
        self.service_name = value
        self.setKeyToSaveToConfig('ServiceName', value)

    # service_is_running.
    @property
    def ServiceIsRunning(self):
        if hasattr(self, 'service_is_running'):
            return getattr(self, 'service_is_running')
        else:
            self.service_is_running = self.getKeyFromConfig(
                'ServiceIsRunning', bool, False)
            return self.service_is_running

    @ServiceIsRunning.setter
    def ServiceIsRunning(self, value):
        self.service_is_running = value
        self.setKeyToSaveToConfig('ServiceIsRunning', value)

    # service_auto_start.
    @property
    def ServiceAutoStart(self):
        if hasattr(self, 'service_auto_start'):
            return getattr(self, 'service_auto_start')
        else:
            self.service_auto_start = self.getKeyFromConfig(
                'ServiceAutoStart', bool, True)
            return self.service_auto_start

    @ServiceAutoStart.setter
    def ServiceAutoStart(self, value):
        self.service_auto_start = value
        self.setKeyToSaveToConfig('ServiceAutoStart', value)

    # #############################

    def Init(self):
        if hasattr(CT_ABC, self.Type):
            type_cls = CT_ABC[self.Type]
            self.TypeInterface = type_cls()

    def Stop(self):
        if self.ServiceIsRunning:
            print("modules stop:" + self.ServiceName)
            self.ServiceIsRunning = False
            try:
                sm.ServicesDeleter(self.OBJECT_PATH)
            except Exception as e:
                print("sm closed...")
            else:
                pass
            finally:
                pass

    def Start(self):
        if self.ServiceIsRunning == False:
            self.ServiceIsRunning = True
            print("modules start:" + self.ServiceName)
            sm.ServicesRegister(self.Type, self.BUS_NAME, self.OBJECT_PATH)
