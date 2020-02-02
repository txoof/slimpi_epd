def __init__():
    pass
# the sections MUST be ordered logically so relative calculations can be made!
# if section 'artist' depends on section 'title' for relative positioning,
# 'artist' MUST be listed AFTER 'title'

twoColumn = {
    'coverart': { # coverart image
                'image': True, # has an image that may need to be resized
                'max_lines': None, # number of lines of text associated with this section
                'padding': 10, # amount of padding at edge
                'width': 1/3, # fraction of total width of display
                'height': 1, # fraction of total height
                'abs_coordinates': (0, 0), # X, Y for top left position of section
                'hcenter': True, # horizontal center-align the contents
                'vcenter': True, # vertically center-align the contents
                'relative': False, # False if position is absolute
                'font': './fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None # font size to use for text
    },
    'title': { # track title
                'image': None, # none if no image is needed
                'max_lines': 3, # number of lines of text associated with this section
                'padding': 10,  # padding at edge
                'width': 2/3, # fraction of total width of display
                'height': 3/5, # fraction of total height of display
                'abs_coordinates': (None, 0), # X, Y for top left position of section
                                          # None indicates that the position is not 
                                          # known and will be calculated 
                                          # relative to another section
                                          # integer indicates an absolute position to use
                'hcenter': False, # horizontal center-align the contents
                'vcenter': True, # vertically center-align the contents
                'relative': ['coverart', 'title'], # [X Section: abs_coordinates+dimension
                                                   #, Y section abs_coordinates+dimension]
                'font': './fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None # font size to use for text

    },
    'artist': { # track artist
                'image': None,
                'max_lines': 2,
                'padding': 10,
                'width': 2/3,
                'height': 1/5,
                'abs_coordinates': (None, None),
                'hcenter': False,
                'vcenter': True,
                'relative': ['coverart', 'title'],
                'font': './fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None
    },
    'album': { #album name
                'image': None,
                'max_lines': 2,
                'padding': 10,
                'width': 2/3,
                'height': 1/5,
                'abs_coordinates': (None, None),
                'hcenter': False,
                'vcenter': True,
                'relative': ['coverart', 'artist'],
                'font': './fonts/Open_Sans/OpenSans-Regular.ttf',
                'font_size': None
    }
}

twoRowSmall = {
    'title': 
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': 2/3,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'relative': False,
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},

    'artist':
            {'image': None,
             'max_lines': 1,
             'padding': 10,
             'width': 1,
             'height': 1/3,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['artist', 'title'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
}

threeRow = {
    'title':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 1,
             'height': 1/2,
             'abs_coordinates': (0, 0),
             'hcenter': True,
             'vcenter': True,
             'relative': False,
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'coverart':
            {'image': True,
             'max_lines': None,
             'padding': 2,
             'width': 2/5,
             'height': 1/2,
             'abs_coordinates': (0, None),
             'hcenter': True,
             'vcenter': True,
             'relative': ['coverart', 'title'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},

    'artist':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 1/4,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'relative': ['coverart', 'title'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None},
    'album':
            {'image': None,
             'max_lines': 2,
             'padding': 10,
             'width': 3/5,
             'height': 3/16,
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
             'height': 1/16,
             'abs_coordinates': (None, None),
             'hcenter': False,
             'vcenter': True,
             'rand': True,
             'relative': ['coverart', 'album'],
             'font': './fonts/Anton/Anton-Regular.ttf',
             'font_size': None}
}


clock = {
  'time':
         {'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1,
          'height': 7/8,
          'abs_coordinates': (0, 0),
          'hcenter': False,
          'vcenter': False,
          'rand': True,
          'inverse': True,
          'relative': False,
          'font': './fonts/Anton/Anton-Regular.ttf',
          'font_size': None},
  'mode':
         {'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1,
          'height': 1/8,
          'abs_coordinates': (0, None),
          'hcenter': False,
          'vcenter': True,
          'rand': True,
          'inverse': True,
          'relative': ['mode', 'time'],
          'font': './fonts/Anton/Anton-Regular.ttf',
          'font_size': None},
}

wordclock = {
  'wordtime':
         {'image': None,
          'max_lines': 3,
          'padding': 10,
          'width': 1,
          'height': 6/7,
          'abs_coordinates': (0, 0),
          'hcenter': False,
          'vcenter': False,
          'rand': True,
          'inverse': True,
          'relative': False,
          'font': './fonts/Anton/Anton-Regular.ttf',
          'font_size': None},
  'time':
         {'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1/2,
          'height': 1/7,
          'abs_coordinates': (0, None),
          'vcenter': True,
          'inverse': True,
          'rand': True,
          'relative': ['time', 'wordtime'],
          'font': './fonts/Anton/Anton-Regular.ttf',
          'font_size': None},
  'mode':
         {'image': None,
          'max_lines': 1,
          'padding': 10,
          'width': 1/2,
          'height': 1/7,
          'abs_coordinates': (None, None),
          'hcenter': False,
          'vcenter': True,
          'rand': True,
          'inverse': True,
          'relative': ['time', 'wordtime'],
          'font': './fonts/Anton/Anton-Regular.ttf',
          'font_size': None},
}

splash =  {
  'app_name':
           {'image': None,
            'max_lines': 1,
            'padding': 10,
            'width': 1,
            'height': 6/10,
            'abs_coordinates': (0, 0),
            'hcenter': True,
            'vcenter': True,
            'rand': False,
            'inverse': False,
            'relative': False,
            'font': './fonts/Anton/Anton-Regular.ttf',
            'font_size': None},

  'version':
          {'image': None,
           'max_lines': 1,
           'padding': 10,
           'width': 1,
           'height': 1/10,
           'abs_coordinates': (0, None),
           'hcenter': True,
           'vcenter': True,
           'rand': False,
           'inverse': False,
           'relative': ['version', 'app_name'],
           'font': './fonts/Dosis/static/Dosis-SemiBold.ttf',
           'maxchar': 20,
           'font_size': None},

  'url':
          {'image': None,
           'max_lines': 2,
           'padding': 10,
           'width': 1,
           'height': 3/10,
           'abs_coordinates': (0, None),
           'hcenter': True,
           'vcenter': True,
           'rand': False,
           'inverse': False,
           'relative': ['url', 'version'],
           'font': './fonts/Dosis/static/Dosis-SemiBold.ttf',
           'maxchar': 35,
           'font_size': None},

}

test = {
  'a':
         {'image': None,
          'max_lines': 3,
          'padding': 10,
          'width': 1,
          'height': 2/5,
          'abs_coordinates': (0, 0),
          'hcenter': True,
          'vcenter': False,
          'rand': False,
          'inverse': False,
          'relative': False,
          'font': './fonts/Open_Sans/OpenSans-SemiBold.ttf',
          'font_size': None},
  'wb':
         {'image': None,
          'max_lines': 3,
          'padding': 0,
          'width': 1,
          'height': 1/5,
          'abs_coordinates': (0, None),
          'vcenter': False,
          'hcenter': False,
          'rand': False,
          'inverse': True,
          'relative': ['wb', 'a'],
          'font': './fonts/Open_Sans/OpenSans-SemiBold.ttf',
          'font_size': None},
  'c1':
         {'image': None,
          'max_lines': 4,
          'padding': 10,
          'width': 1/2,
          'height': 2/5,
          'abs_coordinates': (0, None),
          'hcenter': True,
          'vcenter': True,
          'rand': False,
          'inverse': False,
          'relative': ['c1', 'wb'],
          'font': './fonts/Ubuntu/Ubuntu-Regular.ttf',
          'font_size': None},
  'c2':
         {'image': None,
          'max_lines': 5,
          'padding': 10,
          'width': 1/2,
          'height': 2/5,
          'abs_coordinates': (None, None),
          'hcenter': False,
          'vcenter': True,
          'rand': False,
          'inverse': True,
          'relative': ['c1', 'wb'],
          'font': './fonts/Ubuntu/Ubuntu-Regular.ttf',
          'font_size': None},
}
