from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CleanRegisterForm
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView as DjangoLogoutView

class RegisterView(CreateView):
    form_class = CleanRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = form.cleaned_data.get('role', 'agent')
        user.save()
        return super().form_valid(form)


# class LogoutView(DjangoLogoutView):
#     next_page = reverse_lazy('registration/login')
#
#     def dispatch(self, request, *args, **kwargs):
#         logout(request)
#         request.session.flush()
#         return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect(reverse_lazy('login'))


from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'registration/user_list.html', {'users': users})