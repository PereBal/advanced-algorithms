import os
from functools import partial

from base import BaseController
from spelling_checker.models import TermDictionary


def read(fname, ext, parser, encoding='utf-8'):
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.{ext}'.format(ext=ext):
        raise Exception('Unkown format, .{ext} expected'.format(**locals()))

    with open(fname, 'rt', encoding=encoding) as fd:
        for line in fd:
            yield parser(line.rstrip('\n'))

def upper_parser(line):
    return line.upper()

class SpCheckerController(BaseController):
    def __init__(self, view):
        super(SpCheckerController, self)
        self._file = None
        self._file = os.path.abspath('spelling_checker/data/ES.dic')
        self._dictionary = None
        self._dictionary = TermDictionary(list(read(self._file, ext='dic',
                                              parser=upper_parser,
                                              encoding='latin1')))
        self.view = view

    @classmethod
    def get_instance(cls, view):
        return cls(view)

    def pre_switch(self):
        pass

    def start(self):
        text = self.view.get_text_lines()
        if any(text):
            for suggestions in self.run(text, self._dictionary):
                if suggestions[0]:
                    self.view.notify({
                        'func': 'update_suggestions',
                        'data': {
                            'word': suggestions[1],
                            'suggestions': [suggestion[1]
                                            for suggestion in suggestions[0]],
                        }
                    })


    def file_selected(self, fname):
        self._file = fname if fname else None
        if self._file:
            self._dictionary = TermDictionary(list(read(fname, ext='dic',
                                              parser=upper_parser,
                                              encoding='latin1')))
        self.view.notify({
            'func': 'update_filedata',
            'data': {
                'fname': str(self._file),
                'enable': bool(self._dictionary)
            }
        })

    @staticmethod
    def run(text, term_dictionary):
        # A little magic to rehuse aux_structs and have a clean function call
        suggestions = partial(term_dictionary.suggestions,
                              aux_list=term_dictionary.get_aux_list(),
                              aux_matrix=term_dictionary.get_aux_matrix())

        for line in text:
            if line == '':
                continue
            line = line.upper()
            for word in line.split(' '):
                sug, last = suggestions(word)
                yield (sorted(sug[:last]), word)
