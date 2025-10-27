from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .serializers import LoginSerializer, UserSerializer, PerfilUsuarioSerializer, RegistroPacienteSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    API para login de usuarios
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            # Buscar usuario por email
            user = User.objects.get(email=email)
            # Autenticar con username (Django usa username para authenticate)
            user = authenticate(username=user.username, password=password)
            
            if user and user.perfilusuario.activo:
                user_data = UserSerializer(user).data
                perfil = PerfilUsuarioSerializer(user.perfilusuario).data
                
                return Response({
                    'success': True,
                    'user': user_data,
                    'perfil': perfil,
                    'message': 'Login exitoso'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Credenciales incorrectas o usuario inactivo'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registro_paciente(request):
    """
    API para registro de nuevos pacientes
    """
    serializer = RegistroPacienteSerializer(data=request.data)
    if serializer.is_valid():
        perfil = serializer.save()
        return Response({
            'success': True,
            'message': 'Paciente registrado exitosamente',
            'user_id': perfil.user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    """
    API para obtener el perfil del usuario autenticado
    """
    perfil = PerfilUsuarioSerializer(request.user.perfilusuario).data
    return Response({
        'success': True,
        'perfil': perfil
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    API para logout (limpiar sesión del lado del cliente)
    """
    # En Django REST con SessionAuthentication, el logout se maneja del lado del cliente
    return Response({
        'success': True,
        'message': 'Logout exitoso'
    })