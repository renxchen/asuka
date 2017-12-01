from rest_framework.response import Response


def api_return(status=200, message='', data=''):
    response = \
        {
            'message': message,
            'data': {} if not data else data
        }

    return Response(data=response, status=status)
