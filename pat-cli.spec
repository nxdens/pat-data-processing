# pat-cli.spec
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

a = Analysis(
    ['pat_data_processing/__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('bundle_clean/qc.csv', 'qc.csv'),
        ('bundle_payload/rand.yaml', 'rand.yaml'),
        ('bundle_payload/structure.json', 'structure.json'),
    ],
    hiddenimports=collect_submodules('pat_data_processing'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pat-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
