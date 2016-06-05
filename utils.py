def set_environment():
    # BEGIN virtualenv dynamic import
    import os
    import sys
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '.env', 'py', 'lib')
    if os.path.exists(env_path):
        major, minor = sys.version_info.major, sys.version_info.minor
        zip_path = os.path.join(env_path,
                               'python{major}{minor}.zip'.format(**locals()))
        py_path = os.path.join(env_path,
                               'python{major}.{minor}'.format(**locals()))
        LIBS = [zip_path, py_path] + \
               [os.path.join(py_path, lib) for lib in ('plat-linux',
                                                       'lib-dynload',
                                                       'site-packages')]
        for lib in LIBS:
            sys.path.append(lib)
    else:
        raise RuntimeError('Virtualenv not found at {env_path}.'
                           ''.format(**locals()))
    # END virtualenv dynamic import


def load_ui_form(basedir, name):
    # XXX We're assuming here max-depth of 1 package
    from importlib import import_module
    # Only 1 form per file!
    module = import_module(basedir + '.' + name)
    for key, value in module.__dict__.items():
        if key.startswith('Ui'):
            return value
    raise Exception('Malformed UI file')


def compile_if_needed(fpath):
    # XXX We're assuming here max-depth of 1 package
    import os
    from PyQt5.uic import compileUi
    path = os.path.dirname(fpath)
    package = os.path.basename(path)
    name = os.path.splitext(os.path.basename(fpath))[0]
    ui_name = name + '.ui'
    module = 'ui_' + name
    with open(os.path.join(path, module + '.py'), 'w') as fd:
        compileUi(os.path.join(path, ui_name), fd)

    return (package, module)

def pyqt_set_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()
