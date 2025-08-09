from django.shortcuts import render
from .models import Products, Category
from .serializers import CategorySerializer, ProductsSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics, mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# FBV
@api_view(['GET', ])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response({'status':status.HTTP_200_OK, 'data':serializer.data, 'count':len(category)})


@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        product = Products.objects.all()
        category = request.GET.get('category')
        price = request.GET.get('price')
        if category:
            product = product.filter(category=category)
        if price:
            product = product.filter(price=price)
        search = request.GET.get('search')
        if search:
            product = product.filter(Q(name__icontains=search) | Q(brand__icontains=search))

        ordering = request.GET.get('ordering')
        if ordering:
            product = product.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 2
        product = paginator.paginate_queryset(product, request)

        serializer = ProductsSerializer(product, many=True)
        return paginator.get_paginated_response({'data':serializer.data, 'count':len(product), 'status':status.HTTP_200_OK})
    elif request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED, 'data':serializer.data})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def rud(request, pk):
#     try:
#         product = Products.objects.get(id=pk)
#     except Products.DoesNotExist:
#         return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#     if request.method == 'GET':
#         serializer = ProductsSerializer(product)
#         return Response({'data':serializer.data, 'status': status.HTTP_200_OK})
#     if request.method == 'PUT':
#         serializer = ProductsSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
#         return Response({'error': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
#     if request.method == 'PATCH':
#         serializer = ProductsSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
#         return Response({'status': status.HTTP_400_BAD_REQUEST})
#     if request.method == 'DELETE':
#         product.delete()
#         return Response({'message': 'product deleted','status':status.HTTP_200_OK})


# APIView

# class ProductListCreate(APIView):
#
#     def get(self, request):
#         product = Products.objects.all()
#         category = request.GET.get('category')
#         price = request.GET.get('price')
#         if category:
#             product = product.filter(category=category)
#         if price:
#             product = product.filter(price=price)
#         search = request.GET.get('search')
#         if search:
#             product = product.filter(Q(name__icontains=search) | Q(brand__icontains=search))
#         ordering = request.GET.get('ordering')
#         if ordering:
#             product = product.order_by(ordering)
#
#         paginator = PageNumberPagination()
#         paginator.page_size = 1
#         product = paginator.paginate_queryset(product, request)
#         serializer = ProductsSerializer(product, many=True)
#         return paginator.get_paginated_response({'status':status.HTTP_200_OK, 'data':serializer.data, 'count':len(product)})

#     def post(self, request):
#         serializer = ProductsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_201_CREATED, 'data':serializer.data})
#         return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
# class ProductDetail(APIView):
#
#     def get(self,request, pk):
#         try:
#             product = Products.objects.get(id=pk)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#         serializer = ProductsSerializer(product)
#         return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
#
#     def put(self, request, pk):
#         try:
#             product = Products.objects.get(id=pk)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#         serializer = ProductsSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK, 'updated_data':serializer.data})
#         return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
#
#     def patch(self, request, pk):
#         try:
#             product = Products.objects.get(id=pk)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#         serializer = ProductsSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK, 'updated_data':serializer.data})
#         return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
#
#     def delete(self,request, pk):
#         try:
#             product = Products.objects.get(id=pk)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#         product.delete()
#         return Response({'status':status.HTTP_200_OK, 'message':'product deleted'})

# GenericAPIView

#
# class ProductListCreate(GenericAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#
#     def get(self, request):
#         product = Products.objects.all()
#         category = request.GET.get('category')
#         price = request.GET.get('price')
#         search = request.GET.get('search')
#         ordering = request.GET.get('category')
#         if category:
#             product = product.filter(category=category)
#         if price:
#             product = product.filter(price=price)
#         if search:
#             product = product.filter(Q(name__icontains=search) | Q(brand__icontains=search))
#         if ordering:
#             product = product.order_by(ordering)
#
#         paginator = PageNumberPagination()
#         paginator.page_size = 1
#         product = paginator.paginate_queryset(product, request)
#         serializer = self.serializer_class(product, many=True)
#         return paginator.get_paginated_response({'status':status.HTTP_200_OK, 'data':serializer.data, 'count':len(product)})
#
#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_201_CREATED, 'data':serializer.data})
#         return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

#
# class ProductDetail(GenericAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#
#     def get_object(self, pk):
#         try:
#             return Products.objects.get(pk=pk)
#         except Products.DoesNotExist:
#             return None
#
#     def get(self,request, pk):
#         product = self.get_object(pk)
#         if not product:
#             return Response({'error': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})
#         serializer = self.serializer_class(product)
#         return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
#
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         if not product:
#             return Response({'error':'Product not found', 'status':status.HTTP_404_NOT_FOUND})
#         serializer = self.serializer_class(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': status.HTTP_200_OK, 'updated_data': serializer.data})
#         return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
#
#     def patch(self,request, pk):
#         product = self.get_object(pk)
#         if not product:
#             return Response({'error': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})
#         serializer = self.serializer_class(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': status.HTTP_200_OK, 'updated_data': serializer.data})
#         return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
#
#     def delete(self, request, pk):
#         product = self.get_object(pk)
#         if not product:
#             return Response({'error': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})
#         product.delete()
#         return Response({'status':status.HTTP_200_OK, 'message':'product deleted'})
#

# GenericAPIView with mixins

#
# class ProductListCreate(mixins.ListModelMixin,
#                         mixins.CreateModelMixin,
#                         generics.GenericAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['category', 'price']
#     search_fields = ['name', 'brand']
#     ordering_fields =['name', 'price']
#     ordering = ['name']
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self,request):
#         return self.create(request)
#
# class ProductDetail(mixins.UpdateModelMixin,
#                         mixins.RetrieveModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializer
#
#     def get(self,request, pk):
#         return self.retrieve(request, pk)
#
#     def put(self, request, pk):
#         return self.update(request, pk)
#
#     def patch(self, request, pk):
#         return self.partial_update(request, pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk)
