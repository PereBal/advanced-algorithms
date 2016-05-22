# Convenience function to feed the db with data before the 1st execution
def create_database(dbname):
    import os
    from models import ImageDatabase
    # Fetch the data
    ts_content = []
    base_path = os.path.join('data', 'training_sets')
    for training_dir in os.listdir(base_path):
        dir_path = os.path.join(base_path, training_dir)
        ts_items = []
        for training_set in os.listdir(dir_path):
            ts_items.append(os.path.join(dir_path, training_set))
        ts_content.append({
            training_dir: ts_items
        })

    # Parse it
    db = ImageDatabase.create(dbname)
    for ts_object in ts_content:
        for classname, data in ts_object.items():
            rgb = [0, 0, 0]
            cmyk = [0, 0, 0, 0]
            gray = 0

            for image in data:
                ics = sample(image)
                ics_rgb = ics.rgb_scheme
                ics_cmyk = ics.cmyk_scheme
                ics_gray = ics.gray_scheme

                for i in range(3):
                    rgb[i] += ics_rgb[i]

                for i in range(4):
                    cmyk[i] += ics_cmyk[i]

                gray += ics_gray

            data_len = len(data)
            db.set(classname, {
                'gray': gray // data_len,
                'rgb': [
                    rgb[0] // data_len,
                    rgb[1] // data_len,
                    rgb[2] // data_len
                ],
                'cmyk': [
                    cmyk[0] // data_len,
                    cmyk[1] // data_len,
                    cmyk[2] // data_len,
                    cmyk[3] // data_len,
                ]
            })
    # Store it
    db.save()


def validate(fname):
    return fname


def sample(fname):
    import random as rnd
    from PyQt5.QtGui import QImage
    from models import ImageColorScheme

    image = QImage(validate(fname), str(QImage.Format_RGB32))

    # Start rando-sampliinngggg!!!
    sample_len = 2 * image.byteCount() // 100
    rnd.seed()
    height = image.height() - 1
    width = image.width() - 1
    ics = ImageColorScheme(num_samples=sample_len)
    for i in range(sample_len):
        rheight = rnd.randint(0, height)
        rwidth = rnd.randint(0, width)
        ics.add_pixel(image.pixelColor(rwidth, rheight))
    return ics


def run(dbname, fname, max_results=4):
    from models import ImageDatabase
    database = ImageDatabase(dbname)
    ics = sample(fname)

    rgb = ics.rgb_scheme
    cmyk = ics.cmyk_scheme
    gray = ics.gray_scheme
    return [(entry.distance(), entry.classname)
            for entry in database.get_closest(rgb, cmyk, gray, max_results=4)]


