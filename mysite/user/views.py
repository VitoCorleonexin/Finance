from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'您的账号已经创建成功，请登录!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'user/register.html',{'form':form})


