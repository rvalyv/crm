from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from contacts import views as contact_views
from accounts.views import RegisterView, LogoutView, user_list
from contacts.views import DashboardView
from crm import settings
from deal.views import DealViewSet
from tasks.views import TaskViewSet
from rest_framework.routers import DefaultRouter
from contacts import api as contacts_api

router = DefaultRouter()
router.register(r'api/contacts', contacts_api.ContactViewSet, basename='contact')
router.register(r'api/deals', DealViewSet, basename='deal')
router.register(r'api/tasks', TaskViewSet, basename='tasks')


urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML Views
    path('dashboard/', DashboardView.as_view(template_name='home.html'), name='home'),
    path('leads/', contact_views.LeadListView.as_view(), name='lead-list'),
    path('leads/create/', contact_views.LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/edit/', contact_views.LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', contact_views.LeadDeleteView.as_view(), name='lead-delete'),

    # Authentication - using Django's built-in views
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('dashboard/', DashboardView.as_view(), name='home'),
    path('users/', user_list, name='user-list'),

    path('', include(router.urls)),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('deals/', include('deal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))