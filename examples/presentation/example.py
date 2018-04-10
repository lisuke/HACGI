
from pydbus import SessionBus


bus = SessionBus()
sm = bus.get("com.HACGI.convergence", "/com/HACGI/convergence/ServiceManager")


def cb_signal_sm_service_changed(s_type, service_bus_name, service_obj_path, change_type, new_type):
    if change_type == "register":
        print(s_type, service_bus_name, service_obj_path, change_type, new_type)
        service_type = bus.get(service_bus_name, service_obj_path)
        print(service_type.ServiceName)
        print(service_type.getAllMethodNamesFromInterface("range_selector"))
        print(service_type.getAllMethodNamesFromInterface("switch_interface"))
        import json
        arg_obj = {
            'args': (),
            'kwargs': {}
        }
        arg_json = json.dumps(arg_obj)
        service_type.CallControlInterface(
            'switch_interface', "on", arg_json)

sm.ServicesChanged.connect(cb_signal_sm_service_changed)

from gi.repository import GLib
loop = GLib.MainLoop()
loop.run()
