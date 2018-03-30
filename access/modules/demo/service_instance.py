from base.abstract.service_interface import ServiceInterface
from base.utils.configabc import ConfigABC
from access.dbus import sm
import os


class ServiceInstance(ServiceInterface, ConfigABC):
    """
    <node>
        <interface name='com.HACGI.access.Service'>
        /*
            //
            <property name='BUS_NAME' type='s' access='readwrite'></property>
            <property name='OBJECT_PATH' type='s' access='readwrite'></property>
            //
            <property name='Services' type='a(sa(sso))' access='readwrite' />
            <method name='ServicesRegister'>
                <arg type='s' name='s_type' direction='in' />
                <arg type='s' name='service_bus_name' direction='in' />
                <arg type='o' name='service_obj_path' direction='in' />
                <arg type='i' name='services_all_index' direction='out'/>
            </method>
            <method name='ServicesDeleter'>
                <arg type='o' name='service_obj' direction='in'/>
            </method>
            <method name='GetServiceByIndex'>
                <arg type='i' name='service_obj' direction='in'/>
                <arg type='(sso)' name='service_obj' direction='out'/>
            </method>
            <method name='GetServiceByType'>
                <arg type='s' name='service_obj' direction='in'/>
                <arg type='(sso)' name='service_obj' direction='out'/>
            </method>
            <signal name="ServicesChanged">
                <arg type="s" name="service_type" />
                <arg type="s" name="bus_name" />
                <arg type="o" name="obj_path" />
                <arg type="s" name="change_type" />
                <arg type="b" name="new_s_type" />
            </signal>
            //
            <method name='Quit' />
            <signal name="sm_quit_signal" />
            <signal name="sm_start_signal" />
            */
        </interface>
    </node>
    """
    @property
    def config_file_path(self):
        return os.path.split(os.path.realpath(__file__))[0] + '/service.conf'

    @property
    def config_section(self):
        return "CurrentConfig"

    # dbus bus_name, unique.
    @property
    def BUS_NAME(self):
        if hasattr(self, 'bus_name'):
            return getattr(self, 'bus_name')
        else:
            self.bus_name = self.getKeyFromConfig(
                'BUS_NAME', str, "com.HACGI.access.Service")
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
                'OBJECT_PATH', str, "/com/HACGI/access/Service")
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
        pass

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

    def GetMethod():
        pass

    def CallMethod():
        pass
