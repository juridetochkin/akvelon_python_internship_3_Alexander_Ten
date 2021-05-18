from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('api/v1/', include('api.urls')),
]

