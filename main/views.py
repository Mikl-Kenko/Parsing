from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import json
from .models import DataUser


def pars_user(request):
    '''Функция вывода главной страницы'''
    all_user = DataUser.objects.all().count()
    context = {'all_user': all_user}
    return render(request, 'submit.html', context)


# @csrf_exempt
def ajax(request):
    '''Функция приема данных парсинга по POST и
    записи данных в БД'''
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['data']
        # print(user)
        if DataUser.objects.filter(username=user['username']).count() == 0:
            DataUser.objects.create(name=user['name'],username=user['username'],phone=user['phone'],address_city=user['address']['city'])
            response = {'data': True}
            return JsonResponse(response)
        else:
            raise ValueError

    else:
        raise Http404


def list_user(request):
    '''Функция вывода списка всех username из БД'''
    all_user = DataUser.objects.all()
    context = {'all_user': all_user}
    return render(request, 'list_user.html', context)


def get_user(request, id):
    '''Функция вывода данных из БД, выбранного из списка username'''
    all_user = DataUser.objects.all()
    data_user = DataUser.objects.filter(id=id)
    context = {'all_user': all_user, 'data_user': data_user}
    return render(request, 'user.html', context)






