from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Contact.objects.all()
        return Contact.objects.filter(assigned_to=self.request.user)

    @action(detail=False, methods=['get'])
    def status_counts(self, request):
        queryset = self.get_queryset()
        status_data = queryset.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        return Response(status_data)

    @action(detail=True, methods=['post'])
    def update_notes(self, request, pk=None):
        contact = self.get_object()
        contact.notes = request.data.get('notes', '')
        contact.save()
        return Response({'status': 'notes updated'})