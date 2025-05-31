from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': True, 'user_id': user.id, 'role': user.role, 'message': 'Login successful'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied. Only admins can register users.'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        role = request.data.get('role', 'agent')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, role=role, password=password)
        return Response({'success': True, 'user_id': user.id, 'username': user.username, 'role': user.role}, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class ListUsersAPI(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied. Only admins can list users.'}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all().values('id', 'username', 'role')
        return Response(users, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateAPI(APIView):
    def put(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        is_admin = request.user.role == 'admin'
        is_own_account = request.user.id == target_user.id

        admin_only_fields = {'username', 'password', 'role'}

        if any(field in request.data for field in admin_only_fields) and not is_admin:
            return Response({'error': 'Only admin can update credentials and role'},
                            status=status.HTTP_403_FORBIDDEN)

        update_data = {}
        for field, value in request.data.items():

            if field in admin_only_fields and not is_admin:
                continue

            if field == 'password' and is_admin:
                target_user.set_password(value)
                continue

            if hasattr(target_user, field):
                setattr(target_user, field, value)

        target_user.save()

        return Response({
            'success': True,
            'user_id': target_user.id,
            'updated_fields': list(request.data.keys())
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'No active session'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logout(request)

        return Response(
            {'success': True, 'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )