from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from coreapp.models import Profile, User

from django.db.models import Q
from rest_framework import viewsets
from rest_fremawork.authentication import TokenAuthentication
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


#新規user登録機能
# rest_frameworkから継承
class CreateUserView(generics.CreateAPIView):
    #serializers.pyのUserSerializerへ割り当てる。
    serializer_class = serializers.UserSerializer


# Userがメールアドレスなどの変更をする時に使用する。
# rest_frameworkから継承
class ManageUserView(generics.RetrieveUpdateAPIView):
    #serializers.pyのUserSerializerへ割り当てる。
    serializer_class = serializers.UserSerializer

    #tokenをもとにした認証に使用
    authentication_classes = （authentication.TokenAuthentication,）

    #ログインしたuserのみ利用できるようにする。
    permission_classes = (permissions.IsAuthenticated,)


    # ユーザーの情報を編集するので,getアクセスがされたらuserを返すようにする。
    def get_boject(self):
        return self.request.user


# userの一覧情報を表示していく
class ProfileViewSet(viewsets.ModelViewSet):

    #全要素を取得
    queryset = Profile.objects.all()

    #シリアライザーの割当(profileserializer)
    serializer_class = serializers.ProfileSerializer

    #認証
    #tokenをもとにした認証に使用
    authentication_classes = （authentication.TokenAuthentication,）

    #ログインしたuserのみ利用できるようにする。
    permission_classes = (permissions.IsAuthenticated,)

    #プロフィールを取得するアクション
    # 友達リストに登録されているプロフィールを取得
    def get_queryset(self):
        try:
            is_friend = Profile.objects.get(user=self.request.user)
        except Profile.DoseNotExitst: #プロフィールがなにもない場合
            is_friend = None

        friend_filter = Q() #フィルターを作成
        #Qオブジェクトはモデルのデータの中からor 検索をする時に使われる。

        #フレンド情報からログインをしているユーザーをfriend_filterへ格納している。
        for friend in is_friend.friends.all():
            friend_filter = friend_filter | Q(user=friend)

        #友達に登録されているかを、filterにかけて戻り値とする。
        return self.queryset.filter(friend_filter)

    #プロフィール作成
    # except: IntegrityError:は一人が複数のPFを作成しようとしたときに例外を返している。
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("User can have only one own profile")

