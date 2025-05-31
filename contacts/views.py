from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Contact
from deal.models import Deal
from .forms import ContactForm
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.db.models import Q
from django.urls import reverse_lazy

class LeadListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'leads/list.html'
    context_object_name = 'leads'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Contact.objects.all().select_related('assigned_to', 'created_by').order_by('-created_at')
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            queryset = queryset.filter(assigned_to=self.request.user)

        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(phone__icontains=search_query)
            )

        sort_by = self.request.GET.get('sort', '')
        status_filter = self.request.GET.get('status', '')

        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif status_filter:
            queryset = queryset.filter(status=status_filter)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'leads/create.html'
    success_url = '/leads/'

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'leads/update.html'
    success_url = '/leads/'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            leads = Contact.objects.all()
            deals = Deal.objects.all()
        else:
            leads = Contact.objects.filter(assigned_to=user)
            deals = Deal.objects.filter(created_by=user)

        context['lead_stats'] = {
            'total': leads.count(),
            'new': leads.filter(status='new').count(),
            'contacted': leads.filter(status='contacted').count(),
            'converted': leads.filter(status='converted').count(),
            'failed': leads.filter(status='failed').count(),
            'total_value': leads.aggregate(Sum('deal_price'))['deal_price__sum'] or 0
        }

        context['recent_leads'] = leads.order_by('-created_at')[:6]

        context['status_distribution'] = leads.values('status').annotate(count=Count('id'))

        context['deal_stats'] = {
            'total': deals.count(),
            'open': deals.filter(status='open').count(),
            'won': deals.filter(status='won').count(),
            'lost': deals.filter(status='lost').count(),
        }
        context['deal_status_distribution'] = deals.values('status').annotate(count=Count('id'))

        return context

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'leads/delete_confirm.html'
    success_url = reverse_lazy('lead-list')