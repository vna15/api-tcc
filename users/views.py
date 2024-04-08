from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Users
from .serializers import UsersSerializer


# CRUD user
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):

    if request.method == 'GET':
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=email)
            serializer = UsersSerializer(user)
            return Response(serializer.data)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # Validação de e-mail único
        email = request.data.get('email')
        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Validação de campos obrigatórios
        required_fields = ['email', 'fullName', 'CEP', 'age']
        data = request.data
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({"error": f"{field} is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validação de limites máximos de caracteres
        max_lengths = {'email': 100, 'fullName': 100, 'address': 100}
        for field, max_length in max_lengths.items():
            if field in data and len(data[field]) > max_length:
                return Response({"error": f"{field} exceeds maximum length of {max_length} characters."}, status=status.HTTP_400_BAD_REQUEST)

        # Validação do CEP
        CEP = data.get('CEP')
        if not CEP.isdigit() or len(CEP) != 8:
            return Response({"error": "CEP must contain exactly 8 numeric characters."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validação de limites máximos de caracteres
        max_lengths = {'email': 100, 'fullName': 100, 'address': 100}
        for field, max_length in max_lengths.items():
            if field in request.data and len(request.data[field]) > max_length:
                return Response({"error": f"{field} exceeds maximum length of {max_length} characters."}, status=status.HTTP_400_BAD_REQUEST)

        # Validação do CEP
        CEP = request.data.get('CEP')
        if CEP and (not CEP.isdigit() or len(CEP) != 8):
            return Response({"error": "CEP must contain exactly 8 numeric characters."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
