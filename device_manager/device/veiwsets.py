from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get("status")
        user = self.request.query_params.get("user")
        device_series = self.request.query_params.get("device_series")
        model_name = self.request.query_params.get("model_name")

        if status:
            queryset = queryset.filter(status=status)
        if user:
            queryset = queryset.filter(user__username=user)
        if device_series:
            queryset = queryset.filter(
                device_model__device_series__device_series_name__icontains=device_series
            )
        if model_name:
            queryset = queryset.filter(
                device_model__device_model_name__icontains=model_name
            )

        return queryset

    def homepage(self, request):
        queryset = self.get_queryset()
        context = {"device_list": queryset}
        return render(request, "homepage.html", context)


class UpdateDeviceConfig(generics.RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
