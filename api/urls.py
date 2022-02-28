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
# router.register('userData', views.UserDataApiViewSet)
# router.register('user-register',views.registration_view)


urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.registration_view,name='register')
]