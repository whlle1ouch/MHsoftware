# -*- mode: python -*-

block_cipher = None


a = Analysis(['Software\\venv\\Lib\\site-packages;C:\\Users\\whl\\PycharmProjects\\MH', 'Software\\venv\\Scripts', 'main.py'],
             pathex=['C:\\Users\\whl\\PycharmProjects\\MH', 'C:\\Users\\whl\\PycharmProjects\\MH Software'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MH',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MH')
