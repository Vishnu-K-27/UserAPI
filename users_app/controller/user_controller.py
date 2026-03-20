from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from users_app.model.users import User
from users_app.serializer.user_serializer import UserSerializer
from users_app.utils.user_utils import hash_password
from users_app.utils.user_utils import verify_password
@api_view(['POST'])
def register_user(request):
    name = request.data.get("name")
    email = request.data.get("email")                     
    password = request.data.get("password")

    if not name or not email or not password:
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
     
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    hashed_password = hash_password(password)

    user = User.objects.create(
        name=name,
        email=email,
        password=hashed_password
    )

    

    return Response(
        {"message": "User registered", "data": serializer.data},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def login_user(request):

    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email, is_delete=False)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not verify_password(password, user.password):
        return Response({"error": "Invalid password"}, status=401)
    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(user)

    return Response({
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):

    users = User.objects.filter(is_delete=False)

    serializer = UserSerializer(users, many=True)
    
    return Response({
        "count": len(serializer.data),
        "users": serializer.data
    })
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):

    # Only allow user to update their own profile
    if request.user.id != user_id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=user_id, is_delete=False)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    name = request.data.get("name")
    email = request.data.get("email")

    if name:
        user.name = name

    if email:
        user.email = email

    user.save()

    serializer = UserSerializer(user)

    return Response({
        "message": "User updated",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):

    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.is_delete = True
    user.save()

    return Response({"message": "User deleted successfully"})