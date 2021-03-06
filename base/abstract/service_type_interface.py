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
        self.DeclareMethod("__toJson__")

    def DeclareMethod(self, MethodName):
        self.__cbs__[MethodName] = None

    def RegisterMethod(self, MethodName, cb):
        if MethodName not in self.__cbs__.keys():
            raise ControlMethodNotFoundException(
                "%s was Not Found. You must invoke the DeclareMethod function" % MethodName)
        elif MethodName in self.__cbs__.keys():
            self.__cbs__[MethodName] = cb

    def getAllMethods(self):
        return list(self.__cbs__.keys())

    def InvokeMethods(self, MethodName, *args, **kwargs):
        callback = self.__cbs__[MethodName]
        ret = callback(self, *args, **kwargs)
        return self.toJson()

    def toJson(self):
        return self.__cbs__["__toJson__"](self)


class ServiceTypeInterface(metaclass=ABCMeta):
    """docstring for ServiceTypeInterface"""

    def __init__(self):
        self.interfaces = {}
        self.TypeName = 'unknown'

    def RegisterInterface(self, InterfaceName, Interface):
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

    def HasHoldInterface(self, InterfaceName):
        return InterfaceName in self.interfaces.keys()

    def getAllMethodNamesFromInterface(self, InterfaceName):
        return self.interfaces[InterfaceName].getAllMethods()

    def CallControlInterface(self, InterfaceName, MethodName, arg_JSON_Value):
        import json
        arg_obj = json.loads(arg_JSON_Value)
        args = arg_obj['args']
        kwargs = arg_obj['kwargs']
        args = tuple(args)
        iface = self.interfaces[InterfaceName]
        ret_obj = iface.InvokeMethods(MethodName, *args, **kwargs)
        return json.dumps(ret_obj)

    def getStatus(self):
        ret = []
        for iface in list(self.interfaces.keys()):
            print(iface)
            ret.append(self.interfaces[iface].toJson())
            print(ret)
        return ret


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

    def HasHoldInterface(self, InterfaceName):
        return self.TypeInterface.HasHoldInterface(InterfaceName)

    def CallControlInterface(self, InterfaceName, MethodName, arg_JSON_Value):
        return self.TypeInterface.CallControlInterface(InterfaceName, MethodName, arg_JSON_Value)

    def getAllInterfaces(self):
        return self.TypeInterface.getAllInterfaces()

    def getAllMethodNamesFromInterface(self, InterfaceName):
        return self.TypeInterface.interfaces[InterfaceName].getAllMethods()

    def RegisterMethodToInterface(self, InterfaceName, MethodName, MethodCallback):
        return self.TypeInterface.RegisterMethodToInterface(InterfaceName, MethodName, MethodCallback)

    def getStatus(self):
        import json
        return json.dumps(self.TypeInterface.getStatus())
