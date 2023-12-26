from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager

CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class UserS(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username = models.CharField(verbose_name="username", max_length=15, unique=True)
    data_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='image', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserRefreshToken(models.Model):
    user = models.OneToOneField(UserS, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} - {self.token}"

    