class BaseButtercoinClientError(Exception):
    """
    Base class for all Buttercoin Client errors.
    """

    def __str__(self):
        return self._message


class ButtercoinApiError(BaseButtercoinClientError):
    def __init__(self, api_error):
        super(ButtercoinApiError, self).__init__(api_error)
        self.api_error = api_error
        error = api_error["errors"][0]
        self._message = "Error from Buttercoin API. Details:\n Message: {0}".format(error["message"])
        if "stacktrace_id" in api_error:
            self._message = "{0}\nStacktrace ID: {1}".format(self._message, api_error["stacktrace_id"])
        if "unique_id" in api_error:
            self._message = "{0}\nUnique ID: {1}".format(self._message, api_error["unique_id"])


class InvalidEnvironmentError(BaseButtercoinClientError):
    def __init__(self, message):
        super(InvalidEnvironmentError, self).__init__(message)
        self._message = message