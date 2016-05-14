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
