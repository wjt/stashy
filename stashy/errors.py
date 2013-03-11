from functools import wraps
from decorator import decorator


class NotFoundException(Exception):
    def __init__(self, response):
        try:
            self.data = response.json()
            msg = self.data['errors'][0]['message']
        except ValueError:
            msg = "Not found: " + response.url

        super(NotFoundException, self).__init__(msg)


class GenericException(Exception):
    def __init__(self, response):
        try:
            self.data = response.json()
            msg = "%d: %s" % (response.status_code, self.data)
        except ValueError:
            msg = "Unknown error: " + response.status_code

        super(GenericException, self).__init__(msg)


def maybe_throw(response):
    if not response.ok:
        if response.status_code == 404:
            raise NotFoundException(response)
        else:
            e = GenericException(response)
            try:
                e.data = response.json()
            except ValueError:
                e.content = response.content
            raise e


@decorator
def ok_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.ok


@decorator
def response_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.json()