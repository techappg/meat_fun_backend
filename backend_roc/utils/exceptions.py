from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken as InvalidTokenJWT


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, InvalidTokenJWT):
        custom_response_data = {
            'error': True,
            'data': ['Invalid token']
        }
        response.data = custom_response_data
        return response
    else:
        # print(f"response: {response.data}")
        if response is not None:
            data = response.data
            response.data = {}
            errors = []

            def loop_errors(parent, data):
                for field, value in data.items():
                    if not isinstance(value, list):
                        value = [value]
                    for v in value:
                        errors.append(
                            v.replace("This field", "{} : {} field".format(parent, field))
                        )

            for field, value in data.items():
                if not isinstance(value, list):
                    value = [value]
                for v in value:
                    if isinstance(v, dict):
                        loop_errors(field, v)
                    else:
                        errors.append(str(v).replace("This field", "{} field".format(field)))

            response.data["error"] = True
            response.data["data"] = errors
            return response


class MissingAPIVersion(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'data': ['JWT token is missing']
    }
    default_code = 'not_authenticated'


class TokenError(APIException):
    pass


class InvalidToken(APIException):
    pass