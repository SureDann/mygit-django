from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserS


# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} : {self.id}"


class ShopBajin(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} === {self.shop} === {self.id}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    bajin = models.ForeignKey(ShopBajin, on_delete=models.CASCADE)

    # user = models.ForeignKey(UserS, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} : {self.id}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/articles")

    def __str__(self):
        return f"{self.id} : {self.image}"


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']


class UserToken(models.Model):
    user = models.ForeignKey(UserS, on_delete=models.CASCADE)




