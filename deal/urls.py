from django.urls import path
from .views import DealListView, DealCreateView, DealUpdateView

urlpatterns = [
    path('', DealListView.as_view(), name='deal-list'),
    path('create/', DealCreateView.as_view(), name='deal-create'),
    path('<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
]