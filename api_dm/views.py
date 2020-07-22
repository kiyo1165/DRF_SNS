from rest_framework.permissions import IsAuthenticated
from coreapp.models import Message
from api_dm import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    opermission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

    def perform_create(self, serializer):
        #センダーはログインしている自身（self）である設定
        serializer.save(sender=self.request.user)


# 受信箱
class InboxListView(generics.ListAPIView):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    #認証
    authentication_classes = (TokenAuthentication,)
    opermission_classes = (IsAuthenticated, )

    #自分だけのメッセージを受信できるようにする。
    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)
