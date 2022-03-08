from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register('state', views.StateApiViewSet)
router.register('country', views.CountryApiViewSet)
router.register('complaint-category', views.ComplaintCategoryApiViewSet)
router.register('complaint-sub-category', views.ComplaintSubCategoryApiViewSet)
router.register('municipality', views.MunicipalityApiViewSet)
router.register('complaint', views.ComplaintApiViewSet)
router.register('user-profile',views.UserProfileApiViewSet)
router.register('register',views.UserRegistrationViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]