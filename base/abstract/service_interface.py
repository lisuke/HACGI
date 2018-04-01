from abc import ABCMeta, abstractmethod, abstractproperty


class ServiceInterface(metaclass=ABCMeta):
    """docstring for ServiceInterface"""

    # dbus bus_name, unique.
    @abstractproperty
    def BUS_NAME():
        pass

    # dbus object_path, unique.
    @abstractproperty
    def OBJECT_PATH():
        pass

    # service_type.
    @abstractproperty
    def Type():
        pass

    # service_name.
    @abstractproperty
    def ServiceName():
        pass

    # service_is_running.
    @abstractproperty
    def ServiceIsRunning():
        pass

    # service_auto_start.
    @abstractproperty
    def ServiceAutoStart():
        pass

    #

    @abstractmethod
    def Init():
        pass

    @abstractmethod
    def Stop():
        pass

    @abstractmethod
    def Start():
        pass
