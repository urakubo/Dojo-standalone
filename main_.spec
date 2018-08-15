# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\uraku\\Desktop\\DojoStandalone_',
             'C:\\Users\\uraku\\Desktop\\DojoStandalone_\\Filesystem',
             'C:\\Users\\uraku\\Desktop\\DojoStandalone_\\_dojo',
             'C:\\Users\\uraku\\Desktop\\DojoStandalone_\\Plugins',
             'C:\\Users\\uraku\\Desktop\\DojoStandalone_\\Plugins\\superpixel',
             'C:\\Users\\uraku\\Desktop\\DojoStandalone_\\wxMain'],
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
