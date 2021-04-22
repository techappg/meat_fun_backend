from rest_framework.response import Response


def http_response(error, response, status_code):
    final_response = dict()
    final_response['error'] = error
    if error:
        final_response['data'] = [response]
    else:
        final_response['data'] = response
    return Response(final_response, status_code)
