# WCS
Encrypts a python dict, and stores as binary file. Decrypt is only available to the Windows User that created it (or Admin).

## Description
WCS uses the Windows [Crypt.ProtectData()](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380261(v=vs.85).aspx) API to encrypt a pickled python dictiontary, and store as a binary encrypted file. Only the Windows user that created the crypt store, or a local Admin, can decrypt the data. The WindowsCryptStore class provides dictionary like access to all the key: value pairs stored inside.

## Usage
Creating a new crypt store file
```python
from WCS import CryptStore

wcs = CryptStore.new("secrets.bin")
```

Bind to an existing store file
```python
wcs = CryptStore("secrets.bin")
```

## Security
This class is designed to provide a way to keep data private on a Windows machine, only accessible by the User or the Admin, and without the need for an extra password. It is a balance between security and convenience - you should trust it as much as you trust the machine admins.
Also, this class is mostly a wrapper, so security concerns should be directed towards the Windows API itself.

## Limitations
* Crypt.ProtectData() is available From Windows XP onwards
* Python 2.7 and 3.x supported.

## TODO
Maybe a *nix equivalent, to make it cross compatiable. Suggestions welcomed.

## Trademarks
Just in case its not blindingly obvious, references to Windows are done to aid understanding of the code's purpose and relationaship to the Windows (r) publicly accessible API. It does not infer or suggest anything else.
