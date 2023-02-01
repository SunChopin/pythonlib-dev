# Medical Image Processing Python Library

## Install

```bash
python setup.py install
```

## Usage

```py3
import pylib
path = 'sample.mhd'
img, array = pylib.ReadImage(path)
array = pylib.rot(array, axis='x', angle=90)
pylib.WriteImage(path)
```

Please refer to the [documentation](http://10.7.61.176:1234/docs/html/pylib.html#module-pylib) for more usages.

## Commit

Please read `commit.md` to commit the code to the repository.

