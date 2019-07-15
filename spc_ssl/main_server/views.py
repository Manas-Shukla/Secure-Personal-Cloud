from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
from main_server.forms import sign_up_form,file_upload_form
from main_server.forms import reset_password_form,file_download_form
from main_server.models import registered_clients,global_data

# Create your views here.

#utility function
def buildTree(l):
    if l == "None":
        return l
    Tree = {}
    for i in l:
        if len(i)==1:
            Tree[i[0]] = "None"
            continue
        try:
            Tree[i[0]].append(i[1:])
        except:
            Tree[i[0]] = []
            Tree[i[0]].append(i[1:])

    for k,v in Tree.items():
        Tree[k] = buildTree(v)

    return Tree



def check_server(request):
    if request.session.has_key('id'):
        text = "Working fine"+ ' ' + str(request.session['id'])
        return HttpResponse(text)
    else :
        return HttpResponse('Not working fine')


@csrf_exempt
def sign_up(request):

    if request.method == "POST":
        my_sign_up_form = sign_up_form(request.POST)

        if my_sign_up_form.is_valid():
            #put the data in db
            #security issue will decide later what to do
            username = my_sign_up_form.cleaned_data['username']
            password = hashlib.md5(my_sign_up_form.cleaned_data['password'].encode()).hexdigest()
            try:
                x = registered_clients.objects.get(username=username)
                #y = registered_clients.objects.get(password=password)
                return HttpResponse('#FAIL:Registered Failed try something else as username#')

            except:
                new_client = registered_clients(username=username,password=password)
                new_client.save()

                return HttpResponse('#Successfully Registered#')

        else:
            return HttpResponse('#FAIL:invalid username or password#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')

@csrf_exempt
def reset_password(request):

    if request.method == "POST":
        my_reset_form = reset_password_form(request.POST)

        if my_reset_form.is_valid():
            #put the data in db
            #security issue will decide later what to do
            username = my_reset_form.cleaned_data['username']
            opassword = hashlib.md5(my_reset_form.cleaned_data['old_password'].encode()).hexdigest()
            npassword = hashlib.md5(my_reset_form.cleaned_data['new_password'].encode()).hexdigest()
            try:
                x = registered_clients.objects.get(username=username)
                if opassword == x.password:
                    x.password = npassword
                    x.save()
                    return HttpResponse('#Password Successfully updated#')

                else:
                    return HttpResponse('#FAIL:Wrong password#')

            except:
                return HttpResponse('#FAIL:wrong username#')

        else:
            return HttpResponse('#FAIL:invalid crediantials#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')

@csrf_exempt
def request_for_sync(request):
    if request.method == "POST":
        if request.session.has_key('id'):
            id = request.session['id']
            user = registered_clients.objects.get(id=id)
            if user.is_syncing==True:
                return HttpResponse('#REJECTED')
            else:
                user.is_syncing=True
                user.save()
                return HttpResponse('#ACCEPTED')


        else:

            return HttpResponse('#FAIL:Not Logged In#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')


@csrf_exempt
def request_for_desync(request):
    if request.method == "POST":
        if request.session.has_key('id'):
            id = request.session['id']
            user = registered_clients.objects.get(id=id)
            if user.is_syncing==True:
                user.is_syncing = False
                user.save()

            return HttpResponse('#DONE')


        else:

            return HttpResponse('#FAIL:Not Logged In#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')



@csrf_exempt
def login(request):

    if request.method == "POST":
        my_login_form = sign_up_form(request.POST)

        if my_login_form.is_valid():
            #put the data in db
            #security issue will decide later what to do
            username = my_login_form.cleaned_data['username']
            password = hashlib.md5(my_login_form.cleaned_data['password'].encode()).hexdigest()
            try:
                x = registered_clients.objects.get(username=username)
                if password == x.password:
                    #login in
                    request.session['id'] = x.id
                    #expire the session after 5 minutes of inactivity
                    request.session.set_expiry(300)
                    return HttpResponse('#Successfully Logged in#')

                else:
                    return HttpResponse('#FAIL:Wrong password#')

            except:
                return HttpResponse('#FAIL:wrong username#')

        else:
            return HttpResponse('#FAIL:invalid crediantials#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')

@csrf_exempt
def logout(request):
    try:
        del request.session['id']
    except:
        pass
    return HttpResponse('#Successfully Logged out')



@csrf_exempt
def file_upload(request):

    if request.method == "POST":
        my_file_upload_form = file_upload_form(request.POST,request.FILES)

        if my_file_upload_form.is_valid() or True:

            #file = my_file_upload_form.cleaned_data['file']
            ftype = my_file_upload_form.cleaned_data['ftype']
            fdesc = my_file_upload_form.cleaned_data['fdesc']
            md5sum = my_file_upload_form.cleaned_data['md5sum']
            fname = my_file_upload_form.cleaned_data['fname']
            fpath = my_file_upload_form.cleaned_data['fpath']

            if request.session.has_key('id'):
                id = request.session['id']

                #for now allow same file to be uploaded again will look into it later
                file = request.FILES['file'].read()
                try:

                    entry=global_data.objects.get(user_id=id,
                                                ftype=ftype,
                                                fname=fname,
                                                )
                    if entry.md5sum == md5sum:
                        return HttpResponse('#Already present :: NO CHANGE MADE#')
                    else :
                        entry.file = file
                        entry.md5sum = md5sum
                        entry.save()
                        check_md5 = hashlib.md5(file).hexdigest()
                        return HttpResponse('#File Successfully [Overwritten] md5sum = <' + str(check_md5)+'>#')




                except:

                    check_md5 = hashlib.md5(file).hexdigest()
                    entry = global_data(user_id=id,
                                        ftype=ftype,
                                        md5sum = md5sum,
                                        fname=fname,
                                        fdesc=fdesc,
                                        file=file,
                                        fpath=fpath
                                        )
                    entry.save()
                    return HttpResponse('#File Successfully uploaded md5sum = <' + str(check_md5)+'>#')

            else:
                return HttpResponse('#FAIL:Not Logged In#')
        else:
            return HttpResponse('#FAIL:invalid crediantials#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')

@csrf_exempt
def file_view(request):
    if request.method == "POST":
        if request.session.has_key('id'):
            id = request.session['id']

            #for now allow same file to be uploaded again will look into it later
            entries = global_data.objects.filter(user_id=id).values_list("fpath")
            l = []
            for e in entries:
                l.append(list(e[0].strip().split('/')))
            T = str(buildTree(l))
            return HttpResponse(json.dumps(T))

        else:

            return HttpResponse('#FAIL:Not Logged In#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')

@csrf_exempt
def get_md5(request):
    if request.method == "POST":
        if request.session.has_key('id'):
            id = request.session['id']

            #for now allow same file to be uploaded again will look into it later
            entries = global_data.objects.filter(user_id=id).values_list("fpath","md5sum")
            l = {}
            for e in entries:
                #l.append(list(e[0].strip().split('/')))
                l[e[0].strip()] = e[1].strip()

            #T = str(buildTree(l))
            return HttpResponse(json.dumps(l))

        else:

            return HttpResponse('#FAIL:Not Logged In#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')


@csrf_exempt
def file_download(request):

    if request.method == "POST":
        my_file_upload_form = file_download_form(request.POST)

        if my_file_upload_form.is_valid():

            #file = my_file_upload_form.cleaned_data['file']
            fpath = my_file_upload_form.cleaned_data['fpath']

            if request.session.has_key('id'):
                id = request.session['id']
                # entries = global_data.objects.filter(user_id=id).values_list('fpath')
                # response = {}
                # for e in entries:
                #     if (e[0].strip()).startswith(fpath):
                #         #for now this is wrong need to verify the fpath
                #         ### IMPORTANT ###
                #         try:
                #             response[e[0]] = global_data.objects.get(user_id=id,
                #                             fpath=e[0]).file
                #         except:
                #             continue
                #
                # return HttpResponse(json.dumps(response))
                try:

                    contents = global_data.objects.get(user_id=id,fpath=fpath).file
                    response = HttpResponse(contents)
                    response['Content-Disposition'] = 'attachment;filename=blob.bin'
                    return response
                except:
                    return HttpResponse('#FAIL: No such file on server')


            else:
                return HttpResponse('#FAIL: Not Logged In#')

        else:
            return HttpResponse('#FAIL:invalid crediantials#')
    else:
        return HttpResponse('#FAIL:Get method not allowed#')
