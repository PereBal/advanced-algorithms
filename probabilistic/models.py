import json
from collections import namedtuple
from heapq import heappush, heappop
from math import sqrt

# As this is supposed to be on a mobile device, we'll use __slots__ everywhere
# we can because yea, who needs dynamic attributes

class DBEntry(namedtuple('DBEntry', ['classname', 'rgb', 'cmyk', 'gray'])):
    __slots__ = ()

    def distance(self):
        return (self.rgb + self.cmyk + self.gray) / 3


class ImageDatabase:
    __slots__ = ('_loaded', 'dbname', '_classification')

    # A NoSQL database is assumed to store the images, but for the shake of
    # comprehension and simplicity, we'll use a plain json file.
    def __init__(self, dbname):
        self.dbname = dbname
        self._loaded = {}
        self._classification = {}

    def _classif_table_from_db(self):
        # Load the db if needed
        if not self._loaded:
            with open(self.dbname, 'rt') as fd:
                data = json.load(fd)
            self._loaded = data.get('classification', {})
        return self._loaded

    @classmethod
    def euclidean(self, first, second):
        return sqrt(sum((elem1 - elem2) * (elem1 - elem2)
                        for elem1, elem2 in zip(first, second)))

    @classmethod
    def create(cls, dbname):
        instance = ImageDatabase(dbname)
        instance.save()
        return instance

    def set(self, classname, data):
        self._classification[classname] = {
            'gray': data['gray'],
            'rgb': data['rgb'],
            'cmyk': data['cmyk'],
        }

    def save(self, override=False):
        with open(self.dbname, 'w+') as fd:
            if override:
                classification_table = self._classification
            else:
                try:
                    data = json.load(fd)
                    classification_table = data.get('classification', {})
                    classification_table.update(self._classification)
                except json.decoder.JSONDecodeError:
                    classification_table = self._classification

            json.dump({
                'classification': classification_table
            }, fd)

    # We'll suppose we have a database build with supervised image
    # classification and a table to store/retrieve each family class and its
    # RGB, CMYK, grayscale values.
    #
    # From there we'll calculate the minimum distance between the current
    # picture and the family classes. This is efficient with a reduced amount
    # of classes, but when the number is high, a different approach must be
    # used. For now, we'll stick with brute forcing.
    #
    # Idea from:
    # http://www.sc.chula.ac.th/courseware/2309507/Lecture/remote18.htm
    #
    def get_closest(self, rgb, cmyk, gray, max_results=20):
        classification_table = self._classif_table_from_db()
        items = []
        for classname, entry in classification_table.items():
            gdist = abs(gray - entry['gray'])
            rgbdist = self.__class__.euclidean(rgb, entry['rgb'])
            cmykdist = self.__class__.euclidean(cmyk, entry['cmyk'])

            # Sorts by gray > rgb > cmyk > name. Because of heapq
            # implementation we can't use a db entry here
            dbentry = DBEntry(classname, rgbdist, cmykdist, gdist)
            heappush(items, [dbentry.distance(), dbentry])

        if len(items) > 0:
            for i in range(min(len(items), max_results)):
                yield heappop(items)[1]
        else:
            return []


class ImageColorScheme:
    __slots__ = ('num_samples', 'red', 'green', 'blue', 'cyan', 'magenta',
                 'yellow', 'key', 'gray')

    def __init__(self, num_samples):
        self.num_samples = num_samples
        self.red = self.green = self.blue = 0
        self.cyan = self.magenta = self.yellow = self.key = 0
        self.gray = 0

    @property
    def rgb_scheme(self):
        return (self.red // self.num_samples,
                self.green // self.num_samples,
                self.blue // self.num_samples)

    @property
    def cmyk_scheme(self):
        return (self.cyan // self.num_samples,
                self.magenta // self.num_samples,
                self.yellow // self.num_samples,
                self.key // self.num_samples)

    @property
    def gray_scheme(self):
        return self.gray // self.num_samples

    def add_pixel(self, px_color_scheme):
        rgb = px_color_scheme.getRgb()
        cmyk = px_color_scheme.getCmyk()
        self.gray += int(.3 * rgb[0] + .6 * rgb[1] + .1 * rgb[2])

        self.red += rgb[0]
        self.green += rgb[1]
        self.blue += rgb[2]

        self.cyan += cmyk[0]
        self.magenta += cmyk[1]
        self.yellow += cmyk[2]
        self.key += cmyk[3]
