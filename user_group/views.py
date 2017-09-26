from rest_framework import viewsets
from rest_framework import permissions

from deep.permissions import ModifyPermission

from .models import UserGroup, GroupMembership
from .serializers import UserGroupSerializer, GroupMembershipSerializer


class UserGroupViewSet(viewsets.ModelViewSet):
    serializer_class = UserGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          ModifyPermission]

    def get_queryset(self):
        return UserGroup.get_for(self.request.user)


class GroupMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMembershipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          ModifyPermission]

    def get_queryset(self):
        return GroupMembership.get_for(self.request.user)
