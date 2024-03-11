from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import status, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

#
# class SnippetList(generics.ListCreateAPIView):
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     """
#     List all snippets, or create a new snippet
#     """
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class SnippetDetail(
#     generics.RetrieveUpdateDestroyAPIView
# ):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     """
#     Retrieve, update or delete a snippet
#     """

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request,*args,**kwargs):
        snippet= self.get_object()
        return Response(snippet.highlight())

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    """
    this viewset automatically provides `list`, `create` actions and `retrieve`
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users':reverse('user-list', request=request, format=format),
        'snippets':reverse('snippet-list', request=request, format=format)
    })

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request , *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)