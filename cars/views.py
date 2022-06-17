from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import (
    IsAdminOrReadOnly
)
from .filters import CarFilter
from .models import (
    Type, Brand, Car
)
from .serializers import (
    TypeSerializer,
    BrandSerializer,
    CarViewSerializer,
    CarCreateSerializer
)


class ListCreateTypeAPIView(ListCreateAPIView):
    """
    List all available car types and create new car types
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class TypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete car types
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, *args, **kwargs):
        response = super(TypeRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "Updated successfully."},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super(TypeRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": "Deleted successfully."},
            status=response.status_code
        )


class ListCreateBrandAPIView(ListCreateAPIView):
    """
    List all available car brands and create new car brands
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]


class BrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete car brands
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, *args, **kwargs):
        response = super(BrandRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "Updated successfully."},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super(BrandRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": "Deleted successfully."},
            status=response.status_code
        )


class ListCreateCarAPIView(ListCreateAPIView):
    """
    List all available cars with filter and create new cars
    """
    queryset = Car.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = CarFilter

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.request.method == "GET":
            return CarViewSerializer
        return CarCreateSerializer


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete cars
    """
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.request.method == "GET":
            return CarViewSerializer
        return CarCreateSerializer

    def patch(self, request, *args, **kwargs):
        response = super(CarRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "Updated successfully."},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super(CarRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": "Deleted successfully."},
            status=response.status_code
        )
