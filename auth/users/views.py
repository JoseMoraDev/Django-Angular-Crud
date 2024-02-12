from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime



class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):

    def post(self, request):
        user_mail = request.data['email']
        user_password = request.data['password']
    
        user = User.objects.filter(email=user_mail).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(user_password):
            raise AuthenticationFailed('Wrong password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')

        response = Response()

        # httponly prevents the frontend from accessing the token
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = ({
            'jwt': token
        })

        return response



class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Your are not logged in')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not authenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response