from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, logout, login


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    success_url = '/login/login'
    template_name = 'registration.html'

    def form_valid(self, form):
        form.save(True)
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)
    

class LogoutFormView(FormView):
    def get(self, request):
        logout(request)

        return redirect('/')


class SignInFormView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def get(self, request):
        return render(request, 'login.html', {'form': self.form_class})
    
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)

        return super(SignInFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SignInFormView, self).form_invalid(form)

