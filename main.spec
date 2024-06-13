# main.spec
# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('ocr.py', '.'),
        ('utils.py', '.'),

        # Include Tesseract executable and tessdata directory
        (r'C:\Program Files\Tesseract-OCR\tesseract.exe', 'tesseract'),
        (r'C:\Program Files\Tesseract-OCR\tessdata', 'tessdata'),
    ],
    hiddenimports=['pytesseract', 'pytesseract.pytesseract'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScreenshotApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScreenshotApp',
)
