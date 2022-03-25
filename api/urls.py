from django.urls import path,include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter
from api import views
app_name = 'api'
from .views import ChangePasswordView
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('state', views.StateApiViewSet)
router.register('country', views.CountryApiViewSet)
router.register('complaint-category', views.ComplaintCategoryApiViewSet)
router.register('complaint-sub-category', views.ComplaintSubCategoryApiViewSet)
router.register('municipality', views.MunicipalityApiViewSet)
router.register('complaint', views.ComplaintApiViewSet)
router.register('user-profile',views.UserProfileApiViewSet)
router.register('register',views.UserRegistrationViewSet)
# router.register('approve',views.UserApprovalViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginUserView.as_view()),
    path('api/logout', knox_views.LogoutView.as_view()),
    path('api/logoutall', knox_views.LogoutAllView.as_view()),
    path('user-approve/<int:pk>',views.UserApprovalAPIView.as_view()),
    path('change_password/<int:pk>',ChangePasswordView.as_view()),
]