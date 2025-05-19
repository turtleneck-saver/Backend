from django.http import HttpResponse

from django.views import View
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def test(request):
    return HttpResponse("Hello, world. You're at the polls index.")
