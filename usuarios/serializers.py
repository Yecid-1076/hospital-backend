from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = ['id', 'user', 'rol', 'rol_display', 'telefono', 'fecha_nacimiento', 'activo', 'creado_en', 'actualizado_en']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegistroPacienteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    confirmar_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = ['email', 'password', 'confirmar_password', 'first_name', 'last_name', 'telefono', 'fecha_nacimiento']
    
    def validate(self, data):
        if data['password'] != data['confirmar_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        # Extraer datos del usuario
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        confirmar_password = validated_data.pop('confirmar_password')
        
        # Crear usuario (siempre como paciente)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Crear perfil como paciente
        perfil = user.perfilusuario
        perfil.telefono = validated_data.get('telefono', '')
        perfil.fecha_nacimiento = validated_data.get('fecha_nacimiento', None)
        perfil.rol = 'paciente'  # Siempre paciente por defecto
        perfil.save()
        
        return perfil
    