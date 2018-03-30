from pydbus import SessionBus
from convergence.dbus.service_manager import ServiceManager
from base.global_config import SM__BUS_NAME, SM__OBJECT_PATH
import signal
from convergence import loop


def receive_signal(signum, stack):
    if signum == signal.SIGINT:
        print('Received:', "sigint")
        sm.sm_quit_signal()
        # import time
        # time.sleep(3)
        loop.quit()
        raise SystemExit('Exiting')


def init():
    print('start convergence.dbus')
    print('use session.')
    session_bus = SessionBus()
    global sm
    sm = ServiceManager()
    print('published bus_name: ', SM__BUS_NAME)
    session_bus.publish(SM__BUS_NAME, (SM__OBJECT_PATH, sm))
    signal.signal(signal.SIGINT, receive_signal)
    sm.sm_start_signal()
    # session_bus.subscribe(object=dbus_filter, signal_fired=cb_signal_emission)
