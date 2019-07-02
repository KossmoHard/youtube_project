from django.urls import path
from django.conf.urls import url
from .views import *
from accounts.views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index_list_url'),
    path('registration/', RegistrationFormView.as_view(), name='registration_url'),
    path('login/', LoginFormView.as_view(), name='login_url'),
    path('logout/', AccountLogoutView.as_view(), name='logout_url'),
    path('liked-videos/', LikedVideosListView.as_view(), name='liked_videos_url'),
    path('detail/<str:pk>/', VideoDetailView.as_view(), name='detail_video_url'),
    url('like/', like, name='like')
]
