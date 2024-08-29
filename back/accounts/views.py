from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializer

User = get_user_model()

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if user != request.user:
            return Response(status=403)
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    user = request.user

    if user == user_to_follow:
        return Response({"detail": "You cannot follow yourself."}, status=400)

    if user_to_follow.followers.filter(pk=user.pk).exists():
        user_to_follow.followers.remove(user)
        is_follow = False
    else:
        user_to_follow.followers.add(user)
        is_follow = True

    return Response({"is_follow": is_follow}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_followed(request, username):
    user = request.user
    user_to_follow = get_object_or_404(User, username=username)
    if user.username == user_to_follow.username:
        return Response({"detail": "You cannot follow yourself."}, status=400)
    if user_to_follow.followers.filter(username=user.username).exists():
        is_following = True
    else:
        is_following = False
    return Response({'is_following': is_following})


@api_view(['GET'])
def user(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)