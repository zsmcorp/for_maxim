# Rest Framework
from rest_framework.response import Response
from rest_framework import status


class Responses:
    @staticmethod
    def make_response(data: dict = None, status_code=status.HTTP_200_OK, message: str = None, error: bool = False
                      ) -> Response:
        response = {
            "error": error,
            "message": message,
            "data": data,
            "status_code": status_code
        }

        return Response(data=response)
