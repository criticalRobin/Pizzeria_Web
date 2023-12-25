from django.shortcuts import render
from .models import Product, Table
from .serializers import ProductSerializer, TableSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fcm_django.models import FCMDevice
# Create your views here.
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableList(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    
@api_view(['POST'])
def update_device_token(request):
    new_token = request.data.get('new_token')
    # Asegúrate de que el ID de usuario y el nuevo token estén presentes
    if not new_token:
        return Response({'status': 'Missing token'}, status=400)

    try:
        device, created = FCMDevice.objects.get_or_create(device_id ='E01', defaults={
            'device_id': 'E01',
            'registration_id': new_token})

        if not created:
            device.registration_id = new_token
            device.save()

        return Response({'status': 'Token updated', 'created': created})

    except device.DoesNotExist:
        return Response({'status': 'User not found'}, status=404)