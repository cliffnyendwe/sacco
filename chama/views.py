from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the web api.") 
    
@csrf_exempt
def digicert(request):
    return HttpResponse("Demonstration of domain control for DigiCert order #01008418") 
