
# Package meta
__title__ = 'WCS'
__version__ = '0.1.0'
__author__ = 'github.com/tantalum7'
__license__ = 'WTFPL'


# Library imports
import win32crypt
import pickle
import time


class CryptStore(object):

    # Reserved key defines
    _CREATION_TIME = "__creationtime__"
    _UPDATE_TIME = "__updatetime__"
    _RESERVED_KEYS = [_CREATION_TIME, _UPDATE_TIME]

    def __init__(self, filepath):
        """
        Simple class which stores a pickleable dict as a binary blob file, encrypted using Windows CryptProtectData().
        This allow it to be automatically decrypted by the Windows user that created the file (and admins).

        To create a new crypt store file, use WCS.new(filepath)
        To bind to an existing crypt store file, use WCS(filepath)
        """
        # type: (str) -> None
        # Store file path in class
        self._filepath = filepath

        # Perform initial file load, and store in class as plain data dict
        self._plain_data = self._load_file(filepath)

    @classmethod
    def new(cls, filepath):
        """ Creates new crypt store file, then returns a WCS instance bound to it """
        # type: (str) -> CryptStore
        # Create a new file with creation time as the only entry
        cls._update_file(filepath, {cls._CREATION_TIME: time.time()})

        # Create a WCS instance, and return it
        return CryptStore(filepath)

    @property
    def update_time(self):
        """ Returns a timestamp of the time of last edit """
        # type: () -> float
        return self._plain_data[self._UPDATE_TIME]

    @property
    def creation_time(self):
        """ Returns a timestamp of the time the file was created """
        # type: () -> float
        return self._plain_data[self._CREATION_TIME]

    def __getitem__(self, key):
        """ Standard dict['item'] accessor """
        # type: (any) -> any
        return self._plain_data[key]

    def __setitem__(self, key, value):
        """ Standard dict['item'] = junk setter"""
        # type: (any, any) -> None
        # If key is in the reserved keys list, raise a KeyError
        if key in self._RESERVED_KEYS:
            raise KeyError("Key ({}) is reserved".format(key))

        # Store the new key, value pair in memory dict
        self._plain_data[key] = value

        # Update the crypt store file
        self._update_file(self._filepath, self._plain_data)

    def __delitem__(self, key):
        """ Standard del dict['item'] deleter"""
        # Delete the key from the memory dict
        del self._plain_data[key]

        # Update the crypt store file
        self._update_file(self._filepath, self._plain_data)

    def __iter__(self):
        """ Standard python iterator method """
        return iter(self._plain_data)

    def __len__(self):
        """ Standard len(dict) counter """
        # type: () -> int
        return len(self._plain_data)

    def items(self):
        """ Standard dict.items() method """
        # type: () -> ItemsView
        return self._plain_data.items()

    def keys(self):
        """ Standard dict.keys() method """
        # type: () -> list(any)
        return self._plain_data.keys()

    def values(self):
        """ Standard dict.values() method """
        # type: () -> list(any)
        return self._plain_data.values()

    @classmethod
    def _load_file(cls, filepath):
        # type: (str) -> dict
        # Open the crypt file in binary mode
        with open(filepath, "rb") as fp:
            # Read the binary file, decrypt it, unpickle into a dict then return it
            return pickle.loads(win32crypt.CryptUnprotectData(fp.read())[1])

    @classmethod
    def _update_file(cls, filepath, plain_data):
        # type: (str, dict) -> None
        with open(filepath, "wb") as fp:
            plain_data[cls._UPDATE_TIME] = time.time()
            fp.write(win32crypt.CryptProtectData(pickle.dumps(plain_data)))
