from django.urls import include, path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('face-detect/', views.FaceDetect.as_view(), name='face_detect'),
    path('change-detect/', views.ChangeDetect.as_view(), name='change_detect'),
    path('user-emotions/', views.UserEmotionViewSet.as_view({'get': 'list'})),
    path('user-keywords/', views.UserKeywordViewSet.as_view({'get': 'list'}))
]
