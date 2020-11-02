# ComparatorApp

Creates a visual diff of two input images.


Usage:

You can extract all Layer Compositions from PSD to PNG files by going to File -> Extract PSD.

This creates a folder that you can rename if you want to put a certain version number in the dropdowns.

Comparison by quickly changing between the input images is possible also with the arrow left/right shortcut keys.

Example directory contains two directories (versions) of demo images.



Dependencies:

```shell
pip install PyQt5
pip install photoshop-python-api
pip install Pillow
```

Compile the app to an EXE file.

```shell
pip install pyinstaller
```

```shell
pyinstaller --onefile --name ComparatorApp app.py
```

Now run the executable dist/ComparatorApp.exe