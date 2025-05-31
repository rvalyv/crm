from django.db.models import Count
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Deal
from .forms import DealForm
from rest_framework import viewsets
from .serializers import DealSerializer
from django.views.generic import TemplateView


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class DealListView(LoginRequiredMixin, ListView):
    model = Deal
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'
    ordering = '-id'

    def get_queryset(self):
        queryset = Deal.objects.select_related('contact', 'created_by').order_by('-id')
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            queryset = queryset.filter(created_by=self.request.user)
        return queryset

class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'deals/deal_form.html'
    success_url = reverse_lazy('deal-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DealUpdateView(LoginRequiredMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'deals/deal_form.html'
    success_url = reverse_lazy('deal-list')

