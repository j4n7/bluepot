# https://stackoverflow.com/questions/739654/how-to-make-function-decorators-and-chain-them-together


def needs_vision(method):
    def wrapper(self, *args, **kwargs):
        if self.is_visible:
            return method(self, *args, **kwargs)
    return wrapper
