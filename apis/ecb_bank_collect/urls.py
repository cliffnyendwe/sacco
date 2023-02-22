from django.conf.urls import include, patterns, url
import views
from rest_framework import routers
router = routers.DefaultRouter()

from .views import (
    ValidateUserView, PostTransactionView
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^rest-framework/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^validate_user/(?P<membership_code>.+)/$', ValidateUserView.as_view(), name='validate-user'),
    url(r'^post_transaction/$', PostTransactionView.as_view(), name='post-transaction'),  
]
