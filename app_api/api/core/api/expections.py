from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):  # custom exception handler
    handlers = {
        'ValidationError': _handle_validation_error,
        'Http404': _handle_404_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error
    }  # dict handlers
    response = exception_handler(exc, context)
    if response is not None:
        response['status_code'] = response.status_code
    # if 'UsersTools' in str(context['view']):
    #     print(context)
    exception_class = exc.__class__.__name__  # class name exception
    # print(exception_class, response, response.data, response.context_data)

    if exception_class in handlers:  # if exception class in handlers, call the function

        return handlers[exception_class](exc, context, response)
    return response


def _handle_validation_error(exception, context, response):  # custom validation error handle
    response.data = {
        'message': response.data,
        'status_code': response.status_code,
        'error': True
    }
    return response


def _handle_generic_error(exception, context, response):
    return response


def _handle_404_error(exception, context, response):  # custom 404 error handle
    response.data = {
        'status_code': response.status_code,
        'message': 'this page is not found'
    }
    return response


def _handle_authentication_error(exception, context, response):  # custom authentication error handle
    response.data = {
        'message': 'Please login to proceed',
        'status_code': response.status_code
    }

    return response
