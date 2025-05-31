from django.urls import path
import views

urlpatterns = [
    path('contacts/', views.ContactListAPIView.as_view()),
    path('contacts/create/', views.ContactCreateAPIView.as_view()),
    path('contacts/<int:pk>/', views.ContactDetailAPIView.as_view()),
]