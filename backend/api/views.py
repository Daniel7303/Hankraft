from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from decouple import config
from .models import GalleryImage, Service
from .serializers import GalleryImageSerializer, ServiceSerializer

# ============================================
# PUBLIC ENDPOINTS (No Auth Required)
# ============================================

@api_view(['GET'])
@permission_classes([AllowAny])
def public_gallery(request):
    """Get all active gallery images for public site"""
    images = GalleryImage.objects.filter(is_active=True)
    serializer = GalleryImageSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_services(request):
    """Get all active services for public site"""
    services = Service.objects.filter(is_active=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

# ============================================
# ADMIN AUTHENTICATION
# ============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """Admin login with credentials from .env"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    env_username = config('ADMIN_USERNAME')
    env_password = config('ADMIN_PASSWORD')
    
    if username == env_username and password == env_password:
        user, created = User.objects.get_or_create(
            username=env_username,
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        if created:
            user.set_password(env_password)
            user.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        })
    
    return Response({
        'success': False,
        'message': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

# ============================================
# ADMIN GALLERY CRUD (Auth Required)
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_gallery_list(request):
    """Get all gallery images (including inactive)"""
    images = GalleryImage.objects.all()
    serializer = GalleryImageSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def admin_gallery_create(request):
    """Upload new gallery image"""
    serializer = GalleryImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Image uploaded successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def admin_gallery_update(request, pk):
    """Update gallery image"""
    try:
        image = GalleryImage.objects.get(pk=pk)
    except GalleryImage.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GalleryImageSerializer(image, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Image updated successfully'
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_gallery_delete(request, pk):
    """Delete gallery image"""
    try:
        image = GalleryImage.objects.get(pk=pk)
        image.delete()
        return Response({
            'success': True,
            'message': 'Image deleted successfully'
        })
    except GalleryImage.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)

# ============================================
# ADMIN SERVICES CRUD (Auth Required)
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_services_list(request):
    """Get all services (including inactive)"""
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_service_create(request):
    """Create new service"""
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Service created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def admin_service_update(request, pk):
    """Update service"""
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Service not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ServiceSerializer(service, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Service updated successfully'
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_service_delete(request, pk):
    """Delete service"""
    try:
        service = Service.objects.get(pk=pk)
        service.delete()
        return Response({
            'success': True,
            'message': 'Service deleted successfully'
        })
    except Service.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Service not found'
        }, status=status.HTTP_404_NOT_FOUND)