import abc
from PyQt5 import QtWidgets
class BaseWidgetView(QtWidgets.QWidget):
    __metaclass__ = abc.ABCMeta

    def notify(self, kwargs):
        u"""
        Name based notification with callable() validation
        """
        func_name = kwargs.pop('func')
        func = getattr(self, func_name)

        if not func:
            raise AttributeError('Unknown function to notify '
                                 '{}'.format(func_name))

        if not callable(func):
            raise RuntimeError('{} is not a function'.format(func_name))

        func(**kwargs.pop('data'))

    def display_error(self, cls='Error', level=0, message=''):
        dialog = QtWidgets.QErrorMessage(parent=self)
        dialog.showMessage('{cls}-{level}: {message}'.format(**locals()))

    @classmethod
    @abc.abstractmethod
    def as_view(cls, parent, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def setup_ui(self):
        raise NotImplementedError()


class BaseController(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def get_instance(cls, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def pre_switch(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()
