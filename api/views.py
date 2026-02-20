from rest_framework.response import Response
from rest_framework.decorators import api_view
from utangerapp.models import *
from .serializers import *
# from utangerapp.models import UtangsToUser, UtangsByUser
# from .serializers import UtangsToUserSerializer, UtangsByUserSerializer

# update api endpoints

@api_view(['GET'])
def getUtangsToUser(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    utangsToUser = Utang.objects.filter(utangs=request.user, isUtangToUser=True)

    serializer = UtangSerializer(utangsToUser, many=True)
    return Response(serializer.data, status=200)

# @api_view(['GET'])
# def getUtangsToUser(request):
#     if not request.user.is_authenticated:
#         return Response({"error": "Authentication required"}, status=401)
    
#     utangsToUser = UtangsToUser.objects.filter(users_utangs_to_users=request.user)
        
#     serializer = UtangsToUserSerializer(utangsToUser, many=True)
#     return Response(serializer.data, status=200)

@api_view(['GET'])
def getUtangsByUser(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authenticated required'}, status=401)
    
    utangsByUser = Utang.objects.filter(utangs=request.user, isUtangToUser=False)

    serializer = UtangSerializer(utangsByUser, many=True)
    return Response(serializer.data, status=200)

# @api_view(['GET'])
# def getUtangsByUser(request):
#     if not request.user.is_authenticated:
#         return Response({"error": "Authentication required"}, status=401)
    
#     utangsByUser = UtangsByUser.objects.filter(users_utangs_by_users=request.user)

#     serializer = UtangsByUserSerializer(utangsByUser, many=True)
#     return Response(serializer.data, status=200)

@api_view(['POST'])
def addUserUtang(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)

    name = request.data.get('name')
    amount = request.data.get('amount')
    email = request.data.get('email')
    isUtangToUser = request.data.get('isUtangToUser')

    if isUtangToUser:
        utang = Utang.objects.create(name=name, amount=amount, email=email, isUtangToUser=isUtangToUser)
        utang.utangs.add(request.user)

    else:
        utang = Utang.objects.create(name=name, amount=amount, isUtangToUser=isUtangToUser)
        utang.utangs.add(request.user)

    return Response({'message': 'Utang added successfully'}, status=201)

# @api_view(['POST'])
# def addUserUtang(request):
#     if not request.user.is_authenticated:
#         return Response({"error": "Authentication required"}, status=401)
    
#     name = request.POST.get('name')
#     amount = request.POST.get('amount')
#     utang_type = request.POST.get('utang')

#     if utang_type == 'to_user':
#         utang = UtangsToUser.objects.create(name=name, amount=amount)
#         if utang.users_utangs_to_users.filter(id=request.user.id).exists():
#             return Response({"error": "Utang already exists for this user"}, status=400)
#         utang.users_utangs_to_users.add(request.user)
        
#     else: # utang_type == 'by_user'
#         utang = UtangsByUser.objects.create(name=name, amount=amount)
#         if utang.users_utangs_by_users.filter(id=request.user.id).exists():
#             return Response({"error": "Utang already exists for this user"}, status=400)
#         utang.users_utangs_by_users.add(request.user)

#     return Response({"message": "Utang added successfully"}, status=201)

@api_view(['POST'])
def deleteUserUtang(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    utangPk = request.data.get('utangId')

    try:
        utang = Utang.objects.get(pk=utangPk)
        utang.delete()
        return Response({'message': 'Utang deleted successfully'}, status=200)
    except Utang.DoesNotExist:
        return Response({'error': 'Could not find utang'}, status=404)
