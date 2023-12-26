from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('shop_info/', views.shop_list),
    path("shop_in/<int:pk>", views.shop_detail),
    path('product_info/', views.ProductView.as_view()),
    path("snipp_info/", views.SnippView.as_view()),
    path("shop_id_info/<int:pk>/<int:product_id>", views.ShopViewId.as_view()),
    path("shop/", views.ShopView2.as_view()),
    path("prod_info/", views.ProductApiList.as_view()),
    path("prod_info/<int:pk>/", views.ProductApiList.as_view()),
    path("bajin_info/", views.BajinApiList.as_view()),
    path("bajin_info/<int:pk>/", views.BajinApiList.as_view()),
    path("bajin_info/<int:pk>/", views.BajinApiUpdate.as_view()),
    path("product_price/<int:pk>/", views.ProductPriceGet.as_view()),
    path("product_update/<int:pk>/", views.ProductApiUpdate.as_view()),
    path("product_delete/<int:pk>/", views.ProductRetrieveDestroyApi.as_view()),
    path("product_crud/<int:pk>/", views.ProductCRUD.as_view()),
    path("product_pr/", views.ProductListCreateAPIView.as_view()),
    path("product_image/", views.ProductImageListCreateAPIView.as_view()),
    # path("product_viewset/", views.ProductViewSet.as_view({"get": "list"})),
    # path("product_viewset/<int:pk>/", views.ProductViewSet.as_view({"get": "retrieve"})),
    # path("product_viewset/<int:pk>/", views.ProductViewSet.as_view({"put": "update"})),
    # path("product_viewsetruchnoy/", views.ProductViewSetRuchnoy.as_view({"get":"list"})),
    # path("product_viewsetruchnoy/<int:pk>/", views.ProductViewSetRuchnoy.as_view({"get":"retrieve"})),
    path("product_images/", views.ProductImage.as_view()),
    path("product_images/<int:pk>/", views.ProductImage.as_view()),
    path("product_image_patch/<int:pk>/", views.ProductImagePatch.as_view()),
    path("arandzin_images/<int:pk>/", views.ArandzinImage.as_view()),
    path("product_string_get/<str:pk>/", views.ProductStringGet.as_view()),
    path("shok/", views.ProductViewSet2.as_view()),
    path("product_info2/", views.Prod2GetInfoo.as_view()),
    path("product_info2/<int:pk>/", views.Prod2GetRetrieveInfo.as_view()),
    path("user_token_post/", views.UserTokenPost.as_view()),

]
