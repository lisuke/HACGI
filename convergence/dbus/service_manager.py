# from convergence import loop
from base.abstract.manager_interface import ServiceManagerInterface
from pydbus.generic import signal
from base.global_config import SM__BUS_NAME, SM__OBJECT_PATH
import json


class ServiceManager(ServiceManagerInterface):
    """
    <node>
        <interface name='com.HACGI.convergence.ServiceManager'>
            //
            <property name='BUS_NAME' type='s' access='readwrite'></property>
            <property name='OBJECT_PATH' type='s' access='readwrite'></property>
            //
            <property name='Services' type='a(sa(sso))' access='readwrite' />
            <property name='ServicesJSON' type='s' access='readwrite' />
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
        </interface>
    </node>
    """

    BUS_NAME = SM__BUS_NAME
    OBJECT_PATH = SM__OBJECT_PATH

    Services = [("all", [])]
    ServicesChanged = signal()

    @property
    def ServicesJSON(self):
        return json.dumps(self.Services)

    def ServicesRegister(self, s_type, service_bus_name, service_obj_path):
        c_st = False
        c_already = False
        # register op
        for i in self.Services:
            if i[0] == s_type:
                for j in i[1]:
                    if service_obj_path in j:
                        # already registed
                        print('already registed')
                        c_already = True
                if c_already == False:
                    i[1].append((s_type, service_bus_name, service_obj_path))
                    self.ServicesChanged(
                        s_type, service_bus_name, service_obj_path, "register", False)
                c_st = True
        # add new_s_type and register op
        if c_st == False:
            self.Services.append(
                (s_type, [(s_type, service_bus_name, service_obj_path)]))
            self.ServicesChanged(
                s_type, service_bus_name, service_obj_path, "register", True)
        if c_already:
            n = 0
            for i in self.Services[0][1]:
                if service_obj_path in i:
                    return n
                n = n + 1
        # all services
        self.Services[0][1].append(
            (s_type, service_bus_name, service_obj_path))
        return len(self.Services[0][1]) - 1

    def ServicesDeleter(self, service):
        s_type = ""
        for i in self.Services[0][1]:
            if i[2] == service:
                s_type = i[0]
                self.ServicesChanged(*i, "deleter", False)
                print(i)
                self.Services[0][1].remove(i)
        if s_type != "":
            for i in self.Services:
                if i[0] == s_type:
                    for j in i[1]:
                        if j[2] == service:
                            i[1].remove(j)
                            print('remove: ' + service)

    def GetServiceByIndex(self, index):
        return self.Services[0][1][index]

    def GetServiceByType(self, s_type):
        for i in self.Services:
            if i[0] == s_type:
                return i[1]
        return None

    def Quit(self):
        self.sm_quit_signal()
        loop.quit()

    def Start(self):
        self.sm_start_signal()

    sm_quit_signal = signal()
    sm_start_signal = signal()
