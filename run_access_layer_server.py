from access import loop
from access import dbus
from access import modules

if __name__ == "__main__":
    dbus.init()
    modules.modules_init()
    loop.run()
