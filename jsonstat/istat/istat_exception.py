# This file is part of jsonstat.py

from __future__ import print_function
from __future__ import unicode_literals

# jsonstat


class IstatException(Exception):
    # def __init__(self, message, errors):
    #     # Call the base class constructor with the parameters it needs
    #     super(JsonStatException, self).__init__(message)
    #     # Now for your custom code...
    #     self.errors = errors
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
