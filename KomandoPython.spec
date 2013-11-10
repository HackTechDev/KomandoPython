# -*- mode: python -*-
a = Analysis(['KomandoPython.py'],
             pathex=['/home/solomonkane/PYTHON/KomandoPython'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='KomandoPython',
          debug=False,
          strip=None,
          upx=True,
          console=True )
