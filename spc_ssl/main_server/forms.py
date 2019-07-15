from django import forms

class sign_up_form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget = forms.PasswordInput())

class reset_password_form(forms.Form):
    username = forms.CharField(max_length=100)
    old_password = forms.CharField(widget = forms.PasswordInput())
    new_password = forms.CharField(widget = forms.PasswordInput())

class file_upload_form(forms.Form):
    # username = forms.CharField(max_length=100)
    # password = forms.CharField(widget = forms.PasswordInput())
    file = forms.FileField()
    fname = forms.CharField(max_length=100)
    ftype = forms.CharField(max_length=50)
    fdesc = forms.CharField(max_length=1000)
    md5sum = forms.CharField(max_length=50)
    fpath = forms.CharField(max_length=100)

class file_download_form(forms.Form):
    fpath = forms.CharField(max_length=100)
