from django.urls import include, path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('face-detect/', views.FaceDetect.as_view(), name='face_detect'), # POST PARAMS: ENCODED IMAGE, CHOICE=1
    path('change-detect/', views.ChangeDetect.as_view(), name='change_detect'), # POST PARAMS: URL (TAB)
    path('user-emotions/', views.UserEmotionViewSet.as_view({'get': 'list'})),
    path('user-keywords/', views.UserKeywordViewSet.as_view({'get': 'list'}))
]
