from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def faq(request):
    return render(request, 'core/faq.html')