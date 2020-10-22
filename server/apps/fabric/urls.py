from django.urls import path, include
from .views import ChannelView, ChaincodeView
from rest_framework import routers

from django.urls import include, path
from django.conf.urls import url

router = routers.DefaultRouter()
router.register('channel', ChannelView, basename="channel")
router.register('chaincode', ChaincodeView, basename="chaincode")

urlpatterns = [
    url('', include(router.urls))
]


# router.register('log', LogView, basename="log")
# urlpatterns = [
#     path('', include(router.urls)),
#     path('test/', TestView.as_view())
# ]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('token/black/', LogoutView.as_view(), name='token_black'),
#     path('system/', include('apps.system.urls')),
#     path('fabric/', include('apps.fabric.urls')),
#     path('docs/', include_docs_urls(title="接口文档",
#                                     authentication_classes=[], permission_classes=[])),
#     path('', include(router.urls)),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
