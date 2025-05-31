from django.urls import path
from .views import LeadCreateView, LeadListView

urlpatterns = [
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/', LeadListView.as_view(), name='lead-list'),

]