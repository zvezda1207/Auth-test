from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Role, BusinessElement, AccessRoleRule
from .serializers import RoleSerializer, BusinessElementSerializer, AccessRoleRuleSerializer
from .permissions import IsAdminRole


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminRole]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminRole]


class BusinessElementListCreateView(generics.ListCreateAPIView):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAdminRole]


class BusinessElementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAdminRole]


class AccessRoleRuleListCreateView(generics.ListCreateAPIView):
    queryset = AccessRoleRule.objects.select_related('role', 'element').all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdminRole]


class AccessRoleRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessRoleRule.objects.select_related('role', 'element').all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdminRole]
