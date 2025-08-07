from django.urls import path
from .views import *
urlpatterns = [
    # FBV
    # path('', product_list_create),
    # path('rud/<int:pk>/', rud),
    # path('category/', category_list)

    # APIView
    # path('', ProductListCreate.as_view()),
    # path('detail/<int:pk>/', ProductDetail.as_view())

    # GenericAPIView
    # path('', ProductListCreate.as_view()),
    # path('detail/<int:pk>/', ProductDetail.as_view())

    # GenericAPIView with mixins
    path('', ProductListCreate.as_view()),
    path('detail/<int:pk>/', ProductDetail.as_view())
]