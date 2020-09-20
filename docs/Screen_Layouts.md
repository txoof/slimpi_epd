## Screen Layouts
Layouts determine what content is displayed and where on the screen. The layouts are stored in `slimpi/layouts.py`. Layouts are designed to work on any sized screen as they will adapt to the number of pixels available.

Some layouts are too dense with information to fit well on a small display, but they *will* work.

Any of the following information can be displayed on the "Now Playing" screen of slimpi. 
```
'field name': 'Data'
====================

'id': 52005,
'title': "Women's Realm",
'artist': 'Belle and Sebastian',
'coverid': 'd9b0a026',
'duration': 275.513,
'album_id': '5008',
'genre': 'No Genre',
'album': 'Fold Your Hands Child, You Walk Like a Peasant',
'artwork_url': 'http://192.168.178.9:9000/music/d9b0a026/cover.jpg',
'time': 12.4120923690796,
'mode': 'play'
'coverart': '/tmp/com.txoof.slimpi/5008.jpg'
```

Layout element dimensions are calculated based on a single absolute coordinate and must be organized with the absolute coordinate first and then proceed with each logical sub element.

New layouts can be added to `slimpi/layouts.py` by following the examples below. 

Specify an alternative now playing layout in the configuartion file `now_playing = layout_name`.

Slimpi must be restarted for the changes to take effect (CTRL+C for user; `sudo systemctl restart slimpi-daemon`)
```
# Simple Two Row display of track title and artist
twoRow = {
    'title':
        {'image': None,    # `None` for no image, `True` for an image block
         'max_lines': 3,   # integer - maximum number of lines of text this block can contain
         'padding': 10,    # integer - number of pixles to pad between edge of screen and text
         'width': 1,       # real - percentage of width to use for this block (1 = 100%)
         'height': 1/2,    # real - percentage of height to use for this block (1/2 = 50%)
         'abs_coordinates': (0, 0), # tuple of integer - top left coordinate for this block
         'hcenter': True,  # boolean - `True` to center text or image; `False` to left justify
         'vcenter': True,  # boolean - `True` to vertically center text or image; `False` to left justify
         'font': './fonts/Font/font-regular.ttf' # string for relative (or absolute) path to TTF font file
         'font_size': None,# None/integer - None to calculate the font size based on screen size
         'rand': False     # randomly position the text block within the area defined by width/height
         
   'artist':
       {'image: None,
        'max_lines': 2,
        'padding': 10,
        'width': 1,
        'height': 1/2,
        'abs_coordinates': (0, None), # use an X value of 0 (left side of screen), None indicates that the Y will be calculated 
        'relative': ['artist', 'title'] # use the absolute X from 'artist' section and calculated Y value from 'title'
        'hcenter': True,
        'vcenter': True,
        'font': ./font/Font/font-regular.ttf,
        'font_size': None}
}


# Available layout directives 
# directive_name: values - function
# image: True/None - True: this is an image block, None: this is a text block
# max_lines: int - maximum number of lines of text; overflow text will be shown with elipses (...)
# padding: int - number of pixles to pad around the block on all sides
# width: float - percentage of screen to use for width (1 = 100%)
# height: float - percentage of screen to use for height (1 = 100%)
# abs_coordinates: tuple of int (X, Y) - coordinates of top left corner of block; 
#                  (0, 0): X=0, Y=0 - top left corner of screen
#                  (0, None): = X=0, Y=calculated based on block above
# relative: False, list of string ['name1', 'name2'] - calculate the top left coordinate based on block name1 and name 2
#                  use the X value of 'name1' and the Y value of 'name2' to calculate the top left corner of this block
#                  this should reference the block its self if there is an absolute value (see 'artist' above)
# hcenter: True/False - horizontally center contents of block
# vcenter: True/False - vertically center contents of block
# font: string - path to TTF font
# font_size: None/int - use a specific font size, this will prevent calculating a maximum font size for the text block
# rand: True/False - randomly place contents within the area specified by height/width


# More complex three row layout with images multiple horizontal blocks
threeRow = {
    'title':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': 4/7,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'relative': False,
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'coverart':
            {'image': True,          # images will be dynamically resized using the PIL.Image.thumbnail() method to fit
             'max_lines': None,
             'padding': 2,
             'width': 2/5,
             'height': 3/7,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['coverart', 'title'], # use X=0 and Y=bottom of 'title'
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},

    'artist':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 3/14,
             'abs_coordinates': (None, None), # no absolute coordinates 
             'hcenter': False,
             'vcenter': True,
             'relative': ['coverart', 'title'], # use X=right of 'coverart' and Y=bottom of 'title'
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'album':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 2/14,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'relative': ['coverart', 'artist'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'mode':
            {'image': False,
             'max_lines': 1,
             'width': 3/5,
             'height': 1/14,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'rand': True,
             'relative': ['coverart', 'album'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None}
}             
```


```python
%alias mdconvert mdconvert Screen_Layouts.ipynb
%mdconvert
```

    [NbConvertApp] WARNING | pattern 'Screen_Layouts.ipynb' matched no files



```python

```
