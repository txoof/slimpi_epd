# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


def getPathTuples(path):
    myPath = Path(path)
    allEntries = list()
    for entry in list(myPath.glob('*')):
        if Path.is_dir(entry):
            allEntries = allEntries + getPathTuples(entry)
        else:
            allEntries.append((str(entry), str(entry.parent)))
    return allEntries

binDirs = ['./fonts', './images']
binTuples = []
for each in binDirs:
    tuples =(getPathTuples(each))
    for tup in tuples: 
        binTuples.append(tup)
binTuples

block_cipher = None


a = Analysis(['slimpi.py'],
             pathex=['/home/pi/src/slimpi_epd'],
             binaries=binTuples,
             datas=[('constants.py', '.'),
                    ('layouts.py', '.'),
                    ('logging.cfg', '.'),
                    ('slimpi.cfg', '.')],
             hiddenimports=['plugins'],
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
