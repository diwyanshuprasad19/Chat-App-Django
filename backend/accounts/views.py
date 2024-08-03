from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .services import CognitoService
from .models import CustomUser


class UserRegisterView(View):
    @csrf_exempt
    def post(self, request):
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not (phone and username and password):
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        
        try:
            user = CognitoService().register_user(phone, username, password)
            return JsonResponse({'message': 'User registered successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UserLoginView(View):
    @csrf_exempt
    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if not (phone and password):
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        
        try:
            user = CognitoService().login_user(phone, password)
            return JsonResponse({'message': 'Login successful.', 'data': user})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UserLogoutView(View):
    @csrf_exempt
    def post(self, request):
        access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if not access_token:
            return JsonResponse({'error': 'Access token required.'}, status=400)
        
        try:
            CognitoService().logout_user(access_token)
            return JsonResponse({'message': 'Logout successful.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UserDeleteView(View):
    @csrf_exempt
    def post(self, request):
        phone = request.POST.get('phone')

        if not phone:
            return JsonResponse({'error': 'Phone number is required.'}, status=400)
        
        try:
            # Soft delete user in backend
            user = CustomUser.objects.get(phone=phone)
            user.is_active = False
            user.save()
            # Also, remove the user from Cognito
            CognitoService().delete_user(phone)
            return JsonResponse({'message': 'User deleted successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
