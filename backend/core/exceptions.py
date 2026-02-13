from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

from articles.services.exceptions import (
    StateTransitionError,
    NoChangeError,
    CoolingDownError,
    NoSnapshotError,
)

EXCEPTION_STATUS_REGISTRY = {}


def register_exception(exception_class, status_code):
    """
    This function maps exception classes to status codes
    """

    EXCEPTION_STATUS_REGISTRY[exception_class] = status_code


register_exception(StateTransitionError, status.HTTP_409_CONFLICT)
register_exception(NoChangeError, status.HTTP_400_BAD_REQUEST)
register_exception(CoolingDownError, status.HTTP_429_TOO_MANY_REQUESTS)
register_exception(NoSnapshotError, status.HTTP_409_CONFLICT)


def extract_toast_error(data):
    first_error = next(iter(data.values()))

    if isinstance(first_error, list):
        first_error = first_error[0]

    return first_error


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        for exception_class, status_code in EXCEPTION_STATUS_REGISTRY.items():
            if isinstance(exc, exception_class):
                response = Response({"detail": str(exc)}, status=status_code)
                break

    if response is not None:
        toast_error = extract_toast_error(response.data)
        response.data['toast_error'] = toast_error
        response.data['success'] = status.is_success(response.status_code)

    return response
