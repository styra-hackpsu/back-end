from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'user_emotions', views.UserEmotionViewSet)
router.register(r'user_groups', views.UserKeywordViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('detect/', views.FaceDetect.as_view(), name='face_detect'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]