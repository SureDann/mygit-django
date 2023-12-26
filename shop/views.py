from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpRequest, request
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ShopView2(APIView):
    def get(self, request, format=None):
        shop = models.Shop.objects.all()
        serializer = serializers.ShopSerializer(shop, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        uv = models.Product(created_by=self.request.user)
        serializer = serializers.ProductSerializer(uv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def shop_list(request):
    if request.method == "GET":
        objects = models.Shop.objects.all()
        serializer = serializers.ShopAllSerializer(objects, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.ShopAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=201)
        return JsonResponse(serializer.errors, safe=False, status=400)


@csrf_exempt
def shop_detail(request, pk):
    try:
        shop = models.Shop.objects.get(id=pk)
    except shop.DoesNotExis:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = serializers.ShopAllSerializer(shop)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = serializers.ShopAllSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
    elif request.method == "DELETE":
        shop.delete()
        return HttpResponse(status=204)


class ShopView(APIView):

    def get(self, request, format=None):
        data = models.Shop.objects.all()
        serializer = serializers.ShopAllSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ShopAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopViewId(APIView):
    def test(self, pk):
        try:
            shop = models.Shop.objects.prefetch_related('products').get(id=pk)
            return shop
        except models.Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        shop = self.test(pk)
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shop = models.Shop.objects.prefetch_related('products').get(id=pk)
        serializer = serializers.ShopAllSerializer(shop)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.ShopAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippView(APIView):
    def get(self, request, format=None):
        objects = models.Snippet.objects.all()
        serializer = serializers.SnippAllSerializer(objects, many=True)
        print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.SnippAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):
    def get(self, request, format=None):
        data = models.Product.objects.all()
        serializer = serializers.ProductNewSerializer(data, many=True)
        return Response({"posts": serializer.data})

        # def post(self, request, *args, **kwargs):
        #     pk = kwargs.get("pk", None)
        #     if not pk:
        #         return Response({"error":"Method PUT not allowed"})
        #     try:
        #         instance = models.Product.objects.get(pk=pk)
        #     except:
        #         return Response({"error":"Object does not exists"})
        #     serializer = serializers.ProductNewSerializer(data=request.data, instance=instance)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()

        return Response({"post": serializer.data})

    def post(self, request, format=None):
        serializer = serializers.ProductNewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"post": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = models.Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = serializers.ProductNewSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            objects = models.Product.objects.get(pk=pk).delete()
        except:
            return Response({"error": "Object does not exists"})

        serializer = serializers.ProductNewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})


class ProductApiList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductNewSerializer


class ProductApiUpdate(generics.RetrieveUpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductNewSerializer


class ProductRetrieveDestroyApi(generics.RetrieveDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductAllSerializer


class ProductCRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductAllSerializer


class BajinApiList(generics.RetrieveAPIView):
    queryset = models.ShopBajin.objects.all()
    serializer_class = serializers.BajinNewSerializer


class BajinApiUpdate(generics.UpdateAPIView):
    queryset = models.ShopBajin.objects.all()
    serializer_class = serializers.BajinNewSerializer


class ProductPriceGet(APIView):
    def get(self, request, pk):
        prices = models.Product.objects.filter(price__lte=pk)
        print(prices.values_list()[0][2])

        serializer = serializers.ProductNewSerializer(prices, many=True)
        return Response(serializer.data)
        # price = models.Product.objects.filter(price=pk)
        # serializer = serializers.ProductNewSerializer(price, many=True)
        # return Response(serializer.data)


class BajinView(APIView):
    def get(self, request, pk, format=None):
        objects = models.ShopBajin.objects.get(id=pk)
        serializer = serializers.BajinNewSerializer(objects)
        return Response({"danniner": serializer.data})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = models.Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = serializers.ProductNewSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductNew2Serializator


class ProductImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.ProductImages.objects.all()
    serializer_class = serializers.ProductImageSerializator


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductNew2Serializator


class ProductViewSetRuchnoy(viewsets.ModelViewSet):
    def list(self, request):
        queryset = models.Product.objects.all()
        serializer = serializers.ProductNew2Serializator(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.Product.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductNew2Serializator(user)
        return Response(serializer.data)


class ProductImage(APIView):
    def get_object(self, pk):
        try:
            return models.Product.objects.get(pk=pk)
        except:
            return Response("Fail")

    def get(self, request):
        objects = models.Product.objects.all()
        serializer = serializers.ProductSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pk = request.data.get('product_id')
        images_data = request.FILES.getlist('images')

        try:
            product = models.Product.objects.get(pk=pk)
        except models.Product.DoesNotExist:
            return Response("Product does not exis", status=status.HTTP_404_NOT_FOUND)

        for image_data in images_data:
            image_serializer = serializers.ImageSerializer(data={'product': pk, 'image': image_data})
            if image_serializer.is_valid():
                if len(list(images_data)) >= 6:
                    return Response("fail")
                else:
                    image_serializer.save()
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Images uploaded successfully", status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = models.Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = serializers.ProductNewSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def patch(self, request, pk):
        product_object = self.get_object(pk)
        serializer = serializers.ProductSerializer(product_object, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_object = self.get_object(pk)
        serializer = serializers.ProductSerializer(product_object.delete(), data=request.data)
        return Response("Nice")


class ProductImagePatch(APIView):
    def get_object(self, pk):
        try:
            models.ProductImages.objects.get(pk=pk)
        except:
            return Response("DoesNotExist")

    def get(self, request):
        objects = models.ProductImages.objects.all()
        serializer = serializers.ProductSerializer(objects, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        image = models.ProductImages.objects.get(id=pk)
        serializer = serializers.ImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        objects = models.ProductImages.objects.all()
        res = []
        for i in objects.values_list():
            res.append(i[1])
        my_object = models.ProductImages.objects.get(id=pk).delete()
        if res.count(pk) >= 1:
            seriliazer = serializers.ImageSerializer(my_object, data=request.data)
            return Response("Done bro ;)")
        else:
            return Response("You have only one image, you cant delete it, sorry bor ;)")


class ArandzinImage(APIView):
    def get_object(self, pk):
        try:
            return models.ProductImages.objects.filter(product_id=pk)
        except:
            return Response("The product DoesNotExist")

    def get(self, request, pk):
        objects = models.ProductImages.objects.all()
        object = self.get_object(pk)
        res = []
        for i in objects.values_list():
            res.append(i[1])
        print(f"{res.count(pk)}, hesaaa")
        serializer = serializers.ImageSerializer(object, many=True)
        return Response(serializer.data)


class ProductStringGet(APIView):
    def get(self, request, pk):
        object = models.ShopBajin.objects.filter(name=pk)
        seriliazer = serializers.BajinsSerializer(object, many=True)
        return Response(seriliazer.data)


class ProductViewSet2(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductNew2Serializator
    permission_classes = [IsAuthenticated]


class Prod2GetInfoo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        objects = models.Product.objects.all()
        serializer = serializers.ProductNew2Serializator(objects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.ProductNew2Serializator(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request, pk):


class Prod2GetRetrieveInfo(APIView):
    def get_pk(self, pk):
        try:
            models.Product.objects.get(id=pk)
        except:
            return Response("error")

    def get(self, request, pk):
        object = self.get_pk(pk)
        serializer = serializers.ProductNew2Serializator(object)
        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs):
        serializer = serializers.ProductNew2Serializator(data={"user": request.user, "token": request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTokenPost(APIView):
    def post(self, request):
        serializer = serializers.UserTokenSerializer(data=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def your_view(request):
#     return Response({"mess"})