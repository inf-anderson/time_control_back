from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.api.routes.user.index'), name='auth'),
]
