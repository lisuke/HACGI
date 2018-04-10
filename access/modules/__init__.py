from access import loop
import signal
from access.dbus import sm, session_bus
import importlib
from base.abstract.service_interface import ServiceInterface
from base.abstract.type_interface import auto_search_AllControlTypeInterfaces
import importlib

MS = []


def modules_action_on_sm_start():
    print("ci loading")
    auto_search_AllControlTypeInterfaces()
    print("ci loaded")
    print("sm start")
    if len(MS) == 0:
        auto_search_modules()
    for mn, mo in MS:
        # print(mo.ServiceAutoStart)
        if mo.ServiceAutoStart:
            mo.ServiceName = mn
            mo.Init()
            mo.Start()
            from gi.repository import Gio
            # print(type(mo).dbus) # pydbus's a bug, used (,, mo.dbus)
            session_bus.publish(mo.BUS_NAME, (mo.OBJECT_PATH, mo, mo.dbus))


def modules_action_on_sm_stop():
    print("sm stop")
    for mn, mo in MS:
        print(mn, mo)
        if mo.ServiceIsRunning:
            mo.Stop()


def receive_signal(signum, stack):
    if signum == signal.SIGINT:
        print('Received:', "sigint")
        modules_action_on_sm_stop()
        loop.quit()
        raise SystemExit('Exiting')


def auto_search_modules():
    import os

    current_file_abs_path = os.path.dirname(__file__)
    for m_name in os.listdir(current_file_abs_path):
        is_dir = os.path.isdir(current_file_abs_path + '/' + m_name)
        if is_dir and '__' not in m_name:
            m_lib = importlib.import_module('access.modules.' + m_name)
            cls = getattr(m_lib, 'ServiceInstance', None)
            if cls != None:
                instance = cls()
                if isinstance(instance, ServiceInterface):
                    MS.append((m_name, instance))
                    print('modules_find::success: ' + m_name)
                else:
                    print(
                        'modules_find::failed: isinstance(instance, ServiceInterface) .' + m_name)
            else:
                print(
                    'modules_find::failed: getattr(m_lib, "ServiceInstance", None) == None. ' + m_name)


def modules_init():
    # Ctrl + c
    signal.signal(signal.SIGINT, receive_signal)
    #
    sm.sm_start_signal.connect(modules_action_on_sm_start)
    sm.sm_quit_signal.connect(modules_action_on_sm_stop)
    modules_action_on_sm_start()
