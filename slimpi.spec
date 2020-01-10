# -*- mode: python ; coding: utf-8 -*-

import os
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles
binPaths = ['./fonts', './images']
includeBin = []

for eachPath in binPaths:
    allPaths = getListOfFiles(eachPath)
    for files in allPaths:
        includeBin.append((files, files))


block_cipher = None


a = Analysis(['slimpi.py'],
             pathex=['/home/pi/src/slimpi_epd'],
             binaries=includeBin,
             datas=[('constants.py', '.'),
                    ('layouts.py', '.',
                    ('logging.cfg', '.')
                    ('slimpi.cfg', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [('v', None, 'OPTION')],
          exclude_binaries=True,
          name='slimpi',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='slimpi')
