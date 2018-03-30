from abc import ABCMeta, abstractmethod, abstractproperty


class ServiceManagerInterface(metaclass=ABCMeta):
    """docstring for ServiceManagerInterface"""

    # dbus bus_name, unique.
    @abstractproperty
    def BUS_NAME():
        pass

    # dbus object_path, unique.
    @abstractproperty
    def OBJECT_PATH():
        pass

    # a container, contains all services.
    @abstractproperty
    def Services():
        pass

    @abstractmethod
    def ServicesRegister():
        pass

    @abstractmethod
    def ServicesDeleter():
        pass

    @abstractmethod
    def GetServiceByIndex():
        pass

    @abstractmethod
    def GetServiceByType():
        pass
