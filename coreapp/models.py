from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # emailログイン実装
from django.conf import settings

#imagのuploadパスを作成
def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.user.id) + str(instance.nickname)+str(".")+str(ext)])

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email address is must') #入力必須のエラーメッセージ

        user = self.model(email=self.normalize_email(email), **extra_fields) #normalize_email=>すべて小文字へ変換するー
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.id_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
# UserManagerクラスをUserクラスから呼び出す。
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True) #アクティブ判定=Trueだとアカウントを使ってログインできる。
    is_staff = models.BooleanField(default=True) #adminへのアクセス権限

    objects = UserManager()

    # djangoのデフォルトのUserモデルだとUSERNAME_FIELDは名前になっているのでemailへ変更する。
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

class Profile(models.Model):
    nickname = models.CharField(max_length=20)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name = 'user',
        on_delete=models.CASCADE #(CASCADE)大本のUserが削除されるとProfileも削除される
    )
    created_on = models.DateTimeField(auto_now_add=True) #作成日を登録

    #友人だけとDMを打てるようにする。
    #多 対 多の関係を作成している。
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='friends' #友人を選択できるようにしている。
    )

    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.nickname

class Message(models.Model):

    message = models.CharField(max_length=200)

    # ForeignKey：　one 対 多　の関係を表現している。
    #メッセージを送る側
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender' ,
        on_delete=models.CASCADE #(CASCADE)大本のUserが削除されるとProfileも削除される
    )
    #メッセージを受け取る側
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver' ,
        on_delete=models.CASCADE #(CASCADE)大本のUserが削除されるとProfileも削除される
    )

    def __str__(self):
        return self.message
