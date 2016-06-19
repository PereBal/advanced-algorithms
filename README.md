# advanced-algorithms
4rth year subject at the Universitat de les Illes Balears (UIB)

Everything is made with Python3, PyQt5 and some side libs (PyQtGraph, Numpy and
Graphviz)

## Install

1. Clone the repo :P

        git clone https://github.com/PereBal/advanced-algorithms/

2. Install pip, virtualenv and graphviz

        # Arch
        sudo pacman -S virtualenv pip graphviz
        # Ubuntu
        sudo apt-get install virtualenv python3-pip graphviz

3. Create a .env folder

        virtualenv -p /usr/bin/python3 .env

4. Upgrade pip

        .env/bin/pip install --upgrade pip

5. Install the deps

        .env/bin/pip install -r requirements.txt

6. Install Pyqtgraph

        # Get the repo
        git clone https://github.com/pyqtgraph/pyqtgraph /tmp/pyqtgraph
        # Store the package
        cp -r /tmp/pyqtgraph/pyqtgraph .
        # Remove the repo
        rm -fr /tmp/pyqtgraph

7. Generate the uic files

        for uic in $(find . -iname "*_view.py" | grep -v "ui_");
        do
            dn=$(dirname $uic)
            fn=$(basename $uic)
            [ $dn = "." ] && mod="" \
                          || mod="$(dirname $uic)/"
            echo $mod$fn
            .env/bin/python -c "import utils; utils.compile_if_needed(\"$mod$fn\")"
        done

## Launch

    python3 __main__.py

## Structure

1. Nqueens (nqueens). Algorithm about positioning N-Queens (or whatever piece)
   on a NxN board without any of them killing another one. Classical example of
   backtracking.
   To define new pieces, an image and a json is required, just add those to
   `nqueens/data/pictures` and `nqueens/data` and the code will take care of
   everything else. As an example:

        {
            "piece": {
                "id": "Dummy",
                # Positions where the piece kills.
                #
                #    The positions are on format [x, y] and the signs mean:
                #       + :: from piece pos, to the right (if x) or up (if y)
                #       - :: from piece pos, to the left (if x) or down (if y)
                #
                # As a syntaxic sugar, +/-n might be used to specify straight
                # lines or diagonals being:
                #     0,+n -> straight line up
                #     +n,+n -> diagonal right up
                #     +n,0 -> straight line right
                #     +n,-n -> diagonal right down
                #     0,-n -> straight line down
                #     -n,-n -> diagonal left down
                #     -n,0 -> straight line left
                #     -n,+n -> diagonal left up
                #
                #   Note that other combinations like +/-<number>, +/-n
                #   are allowed
                #
                # On the other hand, +/-<number> is used to add or substract
                # from the current position to calculate where the piece kills.
                # For instance:
                #     +2,-1 == 2 cells right, 1 cell down
                #
                "kills": [
                    ["0", "+n"],
                    ["-n", "+n"],
                    ["+2", "-1"]
                ]
            }
        }

2. Algorithm Comparsion (divide\_and\_conquer). Comparsion between a classical
   way of finding the minimum distance between 2 points in a cloud (O(n^2)) and
   the fast version of it (O(log·n), only works if the points have the same
   probability of being on a position
   [see wikipedia](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Space_partitioning)).
   To display the comparsion, I've used PyQtGraph. If you want to specify a
   different dataset, just add the samples on a json (following the provided
   format) and it'll work. As you can see on
   `divide_and_conquer/data/example.json` the format is:

        {
            "points": [
                {"x": ... , "y": ... },
                ...
            ]
        }

3. Shortest path (greedy), implementation of a _greedy_ version of Dijkstra's
   shortest path algorithm. Graphs are defined on a json with a pretty easy to
   understand format and rendered with Graphviz. For example, a graph is
   defined as:

        {
            "nodes": [
                {
                    # Node identificator
                    "id": ..,
                    # Accessible nodes
                    "to": [..],
                    # Weight of accessing those nodes
                    "by": [..]
                },
                ...
            ]
        }

4. Spelling checker (spelling\_checker). Word 'fixing' algorithm (over spanish
   language for now) using the Levensthein distance to compare the likelihood
   of 2 words and an heuristic to offer suggestions. For now it's pretty slow
   because I haven't had time to optimize the dictionary lookups. [A great
   article](http://norvig.com/spell-correct.html) takes a turn and instead
   of matching a word against a dict, it generates all the words at distance 1
   from the desired one and then does a lookup on an in-memory dict. It's a
   much better approach but for now, it is what it is.

5. Image classificator (probabilistic). Algorithm about classifying images
   based on their color scheme. In order to fasten it, a random sampling
   algorithm has been used. On a future version, a NoSQL database would be used
   to store the classess and their schemes, but for now, a plain json is
   enough. The database format is as follows:

        {
            "classification": {
                "<classname>": {
                    "gray": ...,
                    "rgb": [..., ..., ...],
                    "cmyk": [..., ..., ..., ...]
                },
                ...
            }
        }


### Notes
Pyqtgraph is installed locally because it's pip version does not support PyQt5
yet (on 2016-06-19).
