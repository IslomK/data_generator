from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from data_generator.forms import LoginForm


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('schemas')

        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            logout(request)
        except Exception as ex:
            raise ex

        return redirect('login')