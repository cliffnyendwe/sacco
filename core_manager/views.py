from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import RequestContext, loader

def index(request):
    #return HttpResponse("Hello, world. You're at the core index.")
    all_products = None #Product.objects.order_by('-date_created')[:5]
    return render(request, 'core_manager/index.html', {'all_products': all_products, })
