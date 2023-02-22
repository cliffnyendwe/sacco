from django.conf.urls import include, patterns, url
import views
from rest_framework import routers
router = routers.DefaultRouter()
#router.register(r'members_list/(?P<chama_account>.+)/$', views.MembersViewSet.as_view())


#router.register(r'closed_circles', views.ClosedCirclesViewSet)
router.register(r'member_invitations', views.MemberInvitationsViewSet)
#router.register(r'invite_approvals', views.InviteApprovalsViewSet)
#router.register(r'login_user', views.LoginView)

from .views import (
    LoginView, LogoutView, RegisterChamaView, InviteMemberView, RegisterMemberView, \
    UserDetailsView, DeviceIDView, ChangePasswordView, CloseCircleView, MemberSubscriptionsView, \
    UpdateProfileView, ChamaExportPDFView, ForgotPasswordView, CreatePasswordView, ConfirmLoginView,
    ExitCircleView, CardPaymentView, CurrenciesView
)

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^$', views.index, name='index'),
    url(r'^rest-framework/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^register_chama/$', RegisterChamaView.as_view(), name='register_chama'),
    url(r'^invite_member', InviteMemberView.as_view(), name='invite_member'),
    url(r'members_list/(?P<chama_id>.+)/$', views.MembersViewSet.as_view()),
    url(r'transactions_list/(?P<chama_id>.+)/$', views.TransactionsViewSet.as_view()),
    #url(r'^accept_invite', AcceptInviteView.as_view(), name='accept_invite'),
    #url(r'^approve_invite', ApproveInviteView.as_view(), name='approve_invite'),
    url(r'^register_member', RegisterMemberView.as_view(), name='register_member'),
    url(r'^new_card_payment', CardPaymentView.as_view(), name='card_payment'), 
    url(r'^login_user/$', LoginView.as_view(), name='login'),
    url(r'^user/(?P<currency_id>.+)/$', UserDetailsView.as_view(), name='user_details'),
    url(r'^user/$', UserDetailsView.as_view(), name='user_details'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^close_circle/$', CloseCircleView.as_view(), name='close-circle'), 
    url(r'^register/android-device-id/$', DeviceIDView.as_view(), name='android-device-id'),
    url(r'^exit_circle/$', ExitCircleView.as_view(), name='exit-circle'), 
    url(r'^re_login/$', ConfirmLoginView.as_view(), name='re-login'),       
    url(r'^member_subscriptions/(?P<is_closed>.+)/$', MemberSubscriptionsView.as_view(), name='member-subscriptions'),    
    url(r'^change_password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^forgot_password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^create_password/$', CreatePasswordView.as_view(), name='create_password'),
    url(r'^update_profile', UpdateProfileView.as_view(), name='update_profile'),
    url(r'^export_circle/(\d+)/$', ChamaExportPDFView.as_view(), name='circle_pdf'),
    url(r'^currencies_list/$', CurrenciesView.as_view(), name='currencies-list'),
]
