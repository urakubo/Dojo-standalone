# -*- mode: python -*-
import sys
from os import path, pardir
main_dir = os.path.abspath(SPECPATH)

block_cipher = None


a = Analysis(['main.py'],
             pathex=[
				path.join(main_dir, "Filesystem"),
				path.join(main_dir, "_dojo"),
				path.join(main_dir, "Plugins"),
				path.join(main_dir, "Plugins\\superpixel"),
				path.join(main_dir, "wxMain")],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream','pywt._extensions._cwt'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
