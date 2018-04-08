from base.abstract.service_type_interface import ControlInterface

C_ABC = []


def auto_search_AllControlInterfaces():
    import importlib
    import os

    current_file_abs_path = os.path.dirname(__file__)
    for c_name in os.listdir(current_file_abs_path):
        is_dir = os.path.isdir(current_file_abs_path + '/' + c_name)
        if is_dir and '__' not in c_name:
            c_lib = importlib.import_module(
                'base.abstract.control_interface.' + c_name)
            cabc = getattr(c_lib, 'ControlABC', None)
            if cabc != None:
                if issubclass(cabc, ControlInterface):
                    C_ABC.append((c_name, cabc))
                    print('ControlABC_find::success: ' + c_name)
                else:
                    print(
                        'ControlABC_find::failed: isinstance(cabc, ControlInterface) .' + c_name)
            else:
                print(
                    'ControlABC_find::failed: getattr(c_lib, "ControlABC", None) == None. ' + c_name)

    return C_ABC
