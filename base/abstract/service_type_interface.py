from abc import ABCMeta, abstractmethod, abstractproperty


class ControlMethodNotFoundException(AttributeError):
    """docstring for ControlMethodNotFoundException"""

    def __init__(self, message):
        super(ControlMethodNotFoundException, self).__init__()
        self.message = message


class ControlInterface(object):
    """docstring for ControlInterface"""

    def __init__(self, *args, **kwargs):
        super(ControlInterface, self).__init__(*args, **kwargs)
        self.__cbs__ = dict()

    def DeclareMethod(self, MethodName):
        self.__cbs__[MethodName] = None

    def RegisterMethod(self, MethodName, cb):
        if hasattr(__cbs__, MethodName):
            raise ControlMethodNotFoundException(
                "%s was Not Found. You must invoke the DeclareMethod function" % MethodName)
        elif getattr(__cbs__, MethodName, None) is None:
            self.__cbs__[MethodName] = cb

    def getAllMethods(self):
        return list(self.__cbs__.keys())

    def InvokeMethods(self, MethodName, *args, **kwargs):
        return self.__cbs__[MethodName](*args, **kwargs)


class ServiceTypeInterface(metaclass=ABCMeta):
    """docstring for ServiceTypeInterface"""

    def __init__(self):
        self.interfaces = {}

    def RegisterInterface(self, InterfaceName, Interface, holder, **cbs):
        if isinstance(Interface, ControlInterface):
            self.interfaces[InterfaceName] = Interface

    def getAllInterfaces(self):
        return list(self.interfaces.keys())

    def RegisterMethodToInterface(self, InterfaceName, MethodName, MethodCallback):
        if InterfaceName not in self.interfaces.keys():
            raise ControlMethodNotFoundException(
                "%s was Not Found. You must invoke the RegisterInterface function" % InterfaceName)
        iface = self.interfaces[InterfaceName]
        iface.RegisterMethod(MethodName, MethodCallback)

    @abstractmethod
    def HasHoldInterface(self, InterfaceName, ret_has_own):
        pass

    @abstractmethod
    def CallControlInterface(self, InterfaceName, arg_JSON_Value):
        pass


class ServiceTypeController(object):
    """docstring for ServiceTypeController"""

    @property
    def TypeInterface(self):
        if getattr(self, 'type_interface', None) == None:
            raise Exception(
                "setTypeInterface arg must be ServiceTypeInterface")
        else:
            return self.type_interface

    @TypeInterface.setter
    def TypeInterface(self, type_interface):
        if isinstance(type_interface, ServiceTypeInterface):
            self.type_interface = type_interface
        else:
            raise Exception(
                "setTypeInterface arg must be ServiceTypeInterface")

    def HasHoldInterface(self, InterfaceName, ret_has_own):
        return self.TypeInterface.HasHoldInterface(InterfaceName, ret_has_own)

    def CallControlInterface(self, InterfaceName, arg_JSON_Value):
        return self.TypeInterface.CallControlInterface(InterfaceName, arg_JSON_Value)

    def getAllInterfaces(self):
        return self.TypeInterface.getAllInterfaces()
