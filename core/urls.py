from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # User Auth URLS
    path('auth/', include('accounts.urls')),

    # Car Urls
    path('cars/', include('cars.urls')),

    # Order Urls
    path('orders/', include('orders.urls')),

    # Payment Urls
    path('payments/', include('payments.urls'))
]
