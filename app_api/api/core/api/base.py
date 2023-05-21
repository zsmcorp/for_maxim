from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.core.api.responses import Responses


class BaseView(viewsets.ViewSet):
    """
    Base view
    """

    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]


class BaseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]


class CustomUpdateAPIView(UpdateAPIView):
    """
    Custom update view
    """

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    parser_classes = (MultiPartParser, JSONParser)


class CustomCreateAPIView(CreateAPIView):
    """
    Custom create APIView
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Responses.make_response(data=serializer.data)


class CustomTemplateView(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response()
