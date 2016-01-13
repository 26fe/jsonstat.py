#
# jsonstat
#
class JsonStatException(Exception):
    # def __init__(self, message, errors):
    #     # Call the base class constructor with the parameters it needs
    #     super(JsonStatException, self).__init__(message)
    #     # Now for your custom code...
    #     self.errors = errors
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class JsonStatMalformedJson(JsonStatException):
    pass