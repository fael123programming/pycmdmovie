# PyCMDMovie

PyCMDMovie is a Python package that converts images and videos into ASCII art to be printed onto the terminal.

## Installation

You can install PyCMDMovie via pip:
```bash
pip install pycmdmovie
```
# Usage
## Display an Image
```python
from pycmdmovie import display_img

if __name__ == '__main__':
    display_img('my/image/path.png')
```
## Display a Set of Images
```python
from pycmdmovie import display_imgs

if __name__ == '__main__':
    display_imgs('my/images/dir', delay=0, clear=True, infinite=False)
```
## Display a Video
```python
from pycmdmovie import display_video

if __name__ == '__main__':
    display_video('my/video/path.mp4', delay=.5, clear=False, infinite=True)
```