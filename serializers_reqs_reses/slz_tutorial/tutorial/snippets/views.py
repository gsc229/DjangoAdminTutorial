from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

"""
The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
"""
@api_view(['GET', 'POST']) #decorator
def snippet_list(request, format=None):
  """
  List all code snippets, or create a new snippet.
  """
  if request.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    
    serializer = SnippetSerializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)     
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
  """  
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet = Snippet.objects.get(pk=pk)

  except Snippet.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  elif request.method == 'PUT':   

    serializer = SnippetSerializer(snippet, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
""" 
the following experts are from: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/

Wrapping API views
REST framework provides two wrappers you can use to write API views.

The @api_view decorator for working with function based views.
The APIView class for working with class-based views.
These wrappers provide a few bits of functionality such as making sure 
you receive Request instances in your view, and adding context to Response 
objects so that content negotiation can be performed.

The wrappers also provide behaviour such as returning 
405 Method Not Allowed responses when appropriate, and handling
any ParseError exceptions that occur when accessing request.data with malformed input.
"""

"""  
Our instance view is an improvement over the previous example. It's a little more concise, 
and the code now feels very similar to if we were working with the Forms API. 
We're also using named status codes, which makes the response meanings more obvious.
"""

"""  
Notice that we're no longer explicitly tying our requests or responses to a given content type.
request.data can handle incoming json requests, but it can also handle other formats. 
Similarly we're returning response objects with data, but allowing REST framework to render 
the response into the correct content type for us.
"""

"""  
Adding optional format suffixes to our URLs
To take **advantage of the fact that our responses are no longer hardwired to a single content type** 
let's **add support for format suffixes** to our API endpoints. 
Using format suffixes gives us URLs that explicitly refer to a given format, 
and means our API will be able to handle URLs such as http://example.com/api/items/4.json.

Start by adding a format keyword argument to both of the views, like so.

def snippet_list(request, format=None):
and

def snippet_detail(request, pk, format=None):
Now update the snippets/urls.py file slightly, to append a set of format_suffix_patterns in addition to the existing URLs.

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
We don't necessarily need to add these extra url patterns in, but it gives us a simple, clean way of referring to a specific format.
"""