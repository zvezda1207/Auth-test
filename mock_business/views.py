from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
from access_control.permissions import HasAccessPermission

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [HasAccessPermission]
    element_code = 'products'

    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

