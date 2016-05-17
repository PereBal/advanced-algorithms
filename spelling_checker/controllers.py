def read(fname, ext, parser, encoding='utf-8'):
    import os
    if not os.path.exists(fname):
        raise Exception('Unable to locate file {fname}'.format(**locals()))

    elif os.path.splitext(fname)[1] != '.{ext}'.format(ext=ext):
        raise Exception('Unkown format, .{ext} expected'.format(**locals()))

    with open(fname, 'rt', encoding=encoding) as fd:
        for line in fd:
            yield parser(line.rstrip('\n'))

def dummy_parser(line):
    return line

def run(text_fname, dict_fname):
    from functools import partial
    from models import TermDictionary

    dictionary = TermDictionary(list(read(dict_fname, ext='dic',
                                          parser=dummy_parser,
                                          encoding='latin1')))

    # A little magic to rehuse aux_structs and have a clean function call
    suggestions = partial(dictionary.suggestions,
                          aux_list=dictionary.get_aux_list(),
                          aux_matrix=dictionary.get_aux_matrix())

    for line in read(text_fname, ext='txt', parser=dummy_parser):
        for word in line.split(' '):
            sug, last = suggestions(word)
            yield (sorted(sug[:last]), word)
