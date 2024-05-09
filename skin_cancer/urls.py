from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user-dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('user-profile', views.Profile.as_view(), name='profile'),
    # path('user-list', views.User_list.as_view(), name='user-list'),
    
    path('start-predict', views.Start_predict.as_view(), name='start-predict'),
    path('output/', views.output, name='output'),
    # path('user-parkinson-data', views.Parkinson_data_edit.as_view(), name='user-parkinson-data'),
    
    # report pdf generator
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    # path('report/', views.report, name='report'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)