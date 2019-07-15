import base64
import pyDes

from django.shortcuts import render
from main_server.views import sign_up as main_sign_up
from main_server.views import login as main_login
from main_server.views import logout as main_logout
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from main_server.models import registered_clients,global_data
from main_server.views import reset_password as main_reset_password
import re,os
import sys
# Create your views here.
base_path = '/home/mohit/SecurePersonalCloud/'
def sign_up(request):
    if request.method == 'POST':
        msg = main_sign_up(request).content.decode()

        if msg.startswith("#FAIL"):
            return HttpResponse(msg)
        else:
            request.method='GET'
            return redirect(login)
    else:
        return render(request,'sign_up.html')

def login(request):
    if request.method == 'POST':
        res = main_login(request)
        msg = res.content.decode()
        if msg.startswith('#FAIL'):
            return HttpResponse(msg)
        else:
            # user_id = request.session['id']
            # user=registered_clients.objects.get(id=user_id)
            # files=tuple(global_data.objects.filter(user_id=5).values_list("fname","ftype"))
            # return render(request,'logged_in.html',{'username':user.username,'files':files})
            return homepage(request,'')

    else:
        if request.session.has_key('id'):
            # user_id = request.session['id']
            # user=registered_clients.objects.get(id=user_id)
            # files=tuple(global_data.objects.filter(user_id=5).values_list("fname","ftype"))
            # return render(request,'logged_in.html',{'username':user.username,'files':files})
            return homepage(request,'')
        else:
            return render(request,'login.html')

def logout(request):
    main_logout(request)
    request.method='GET'
    return login(request)

def homepage(request,root):
    user_id = request.session['id']
    user=registered_clients.objects.get(id=user_id)
    files=tuple(global_data.objects.filter(user_id=5).values_list("fname","ftype"))
    data=set()
    regex = root + '/(.*?)/'
    regforfile=root+'/(.*)'
    #check for file
    #print(regex)
    for f in files:
        ##### if error then its a file #####
        if(f[0] == root):
            var = global_data.objects.get(user_id=user_id,fname=f[0])
            fname = var.fname
            file_data = str(var.file)
            file_data = file_data[2:]
            file_data = file_data[:-1]

                #file_data=base64.b64decode(file_data)
            return render(request,'view_file.html',{'fname':fname,'file_data':file_data})
        try:
            dir = re.findall(regex,f[0])[0]
        except:
            filename=re.findall(regforfile,f[0])
            if len(filename)>0:
                path='/web_client/homepage/root='+root+'/'+filename[0]
                data.add((filename[0],path,f[1]))
            continue
            #check for file
        next_root = root+'/'+dir
        #url = 'http://localhost:8000/web_client/homepage/root='+next_root
        url = '/web_client/homepage/root='+next_root
        data.add((dir,url,"dir"))

    return render(request,'logged_in.html',{'username':user.username,'data':data})


def reset_password(request):
    if request.method == 'POST':
        msg = main_reset_password(request).content.decode()
        if msg.startswith("#FAIL"):
            return HttpResponse(msg)
        else:
            request.method='GET'
            return redirect(login)
    else:
        return render(request,'reset_password.html')
