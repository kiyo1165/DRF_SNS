from rest_framework import permissions

# このクラスをapi_user.viewsから使用する。
class ProfilePermission(permissions.BasePermission):
    # SAFE_METHODS(GET, HEAD, OPTIONS) が定義されているので、リクエストメソッドがそのどれかであれば True を返します。
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.userpro.id == request.user.id #ログインしている人しかTrueを返さない

class TweetPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.id == request.user.id