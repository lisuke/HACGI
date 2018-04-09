from base.abstract.service_type_interface import ServiceTypeInterface

CT_ABC = []


def auto_search_AllControlTypeInterfaces():
    import importlib
    import os

    current_file_abs_path = os.path.dirname(__file__)
    for ct_name in os.listdir(current_file_abs_path):
        is_dir = os.path.isdir(current_file_abs_path + '/' + ct_name)
        if is_dir and '__' not in ct_name:
            c_lib = importlib.import_module(
                'base.abstract.type_interface.' + ct_name)
            ct_abc_cls = getattr(c_lib, 'ControlTypeABC', None)
            if ct_abc_cls != None:
                if issubclass(ct_abc_cls, ServiceTypeInterface):
                    CT_ABC.append((ct_name, ct_abc_cls))
                    print('ControlTypeABC_find::success: ' + ct_name)
                else:
                    print(
                        'ControlTypeABC_find::failed: isinstance(ct_abc_cls, ServiceTypeInterface) .' + ct_name)
            else:
                print(
                    'ControlTypeABC_find::failed: getattr(c_lib, "ControlTypeABC", None) == None. ' + ct_name)

    return CT_ABC
