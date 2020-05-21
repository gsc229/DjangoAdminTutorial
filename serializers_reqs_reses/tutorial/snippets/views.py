from rest_framework import mixins, generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly

"""
The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
"""
@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
  })


class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = [renderers.StaticHTMLRenderer]
  
  def get(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)


""" GET all, POST   (generics.ListCreateAPIView) """
class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  """ see notes on this property below """
  permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
  """ see notes below on this method """
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
  

""" GET single, PUT, DELETE    (RetrieveUpdateDestroyAPIView) """
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer  
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
  

"""  GET the a list of all users (ListAPIView) """
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

"""  GET single user (RetrieveAPIView) """
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


""" 
perform_create:

Withoug this method, if we created a code snippet, there'd be no way of associating the user that created the snippet,
with the snippet instance. The user isn't sent as part of the serialized representation, but is instead a property of 
the incoming request.

The way we deal with that is by overriding a .perform_create() method on our snippet views, that allows us to
modify how the instance save is managed, and handle any information that is implicit in the incoming request or requested URL.

Udating Our Serializer
In the serializer, we update the owner field to reflect this:
owner = serializers.ReadOnlyField(source='owner.username')

This field is doing something quite interesting. The source argument controls which attribute is used to populate a field, 
and can point at any attribute on the serialized instance. It can also take the dotted notation shown above, in which case 
it will traverse the given attributes, in a similar way as it is used with Django's template language.

"""

"""
permissons property:

Adding required permissions to views:
Now that code snippets are associated with users, we want to make sure that only authenticated users are able to create, update and delete code snippets.

REST framework includes a number of permission classes that we can use to restrict who can access a given view. 
In this case the one we're looking for is IsAuthenticatedOrReadOnly, which will ensure that authenticated requests
get read-write access, and unauthenticated requests get read-only access.

"""