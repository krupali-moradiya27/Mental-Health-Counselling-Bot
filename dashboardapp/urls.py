from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from dashboardapp import views

urlpatterns = [
        path('', views.dashboardFun, name='dashboardPage'),
        path('chat/', views.chatFun, name='chatPage'),
        path('subscription/', views.subscriptionFun, name='subscriptionPage'),
        # path('subscribe/', views.subscribeuserFun, name='subscribeuserPage'),
        path('showreceipt/', views.showreceiptFun, name='showreceiptPage'),       
        path("chat-response/", views.chatbotresponseFun, name="chatbotresponsePage"),
        path("chat-history/<str:session_id>/", views.chathistorybysessionFun, name="chathistorybysessionPage"),
        path("sessions/", views.getusersessionsFun, name="getusersessionsPage"),
        path("new-session/", views.createnewsessionFun, name="createnewsessionPage"),
        path("rename-session/<str:session_id>/", views.renamesessionFun, name='renamesessionPage'),
        path("delete-session/<str:session_id>/", views.deletesessionFun, name='deletesessionPage'),
        path('checkout/', views.checkoutFun, name='checkoutPage'),
        path('payment/success/', views.paymentsuccessFun, name='paymentsuccessPage'),
        path('payment/cancel/', views.paymentcancelFun, name='paymentcancelPage'),
        path('stripe/webhook/', views.stripewebhookFun, name='stripewebhookPage'),
]
