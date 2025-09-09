from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def indexFun(request):
    return render(request, 'index-2.html')

def planFun(request):
    return render(request, 'plans.html')
