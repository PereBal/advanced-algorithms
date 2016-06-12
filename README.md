# advanced-algorithms
4rth year subject at the Universitat de les Illes Balears (UIB)

Everything is made with Python3, PyQt5 and some side libs (pyqtgraph, numpy,
graphviz)

## Install

0. Clone the repo :P
```sh
git clone https://github.com/PereBal/advanced-algorithms/
```
1. Install pip, virtualenv and graphviz
```sh
# Arch
sudo pacman -S virtualenv pip graphviz

# Ubuntu
sudo apt-get install virtualenv python3-pip graphviz
```
2. Create a .env folder
```sh
virtualenv -p /usr/bin/python3 .env
```
3. Upgrade pip
```sh
.env/bin/pip install --upgrade pip
```
4. Install the deps
```sh
.env/bin/pip install -r requirements.txt
```
5. Install Pyqtgraph
```sh
# Get the repo
git clone https://github.com/pyqtgraph/pyqtgraph /tmp/pyqtgraph

# Store the package
cp -r /tmp/pyqtgraph/pyqtgraph .

# Remove the repo
rm -fr /tmp/pyqtgraph
```
5. Generate the uic files
```sh
for uic in $(find -iname "*_view.py" | grep -v "ui_");
do
    dn=$(dirname $uic)
    fn=$(basename $uic)
    [ $dn = "." ] \
    && mod=""     \
    || mod="$(dirname $uic)/"
    echo $mod$fn
    .env/bin/python -c "import utils; utils.compile_if_needed(\"$mod$fn\")"
done
```

## Launch
```sh
python3 __main__.py
```

### Notes
Pyqtgraph is installed locally because it's pip version does not support
PyQt5. To do so:
