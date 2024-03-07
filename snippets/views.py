from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions


class SnippetList(generics.ListCreateAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    List all snippets, or create a new snippet
    """

class SnippetDetail(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    """
    Retrieve, update or delete a snippet
    """


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)