# Contents
A python 3 compatible version of Kernel Temporal Segmentation (KTS) algorithm.

The original codes is written in Python 2 and used _weave_ package which was long deprecated. This repo provides Python 3 compatible version of KTS algo.

# Usage
1. Compile Cython code
```sh
python setup.py build_ext --inplace
```

2. Run demo
```sh
python demo.py
```

# Requirements
```
python>=3.6
matplotlib
Cython
```

# Reference
```
@inproceedings{potapov2014category,
    url = {http://hal.inria.fr/hal-01022967},
    title = {{Category-specific video summarization}},
    author = {Potapov, Danila and Douze, Matthijs and Harchaoui, Zaid and Schmid, Cordelia},
    booktitle = {{ECCV 2014 - European Conference on Computer Vision}},
    year = {2014},
}
```