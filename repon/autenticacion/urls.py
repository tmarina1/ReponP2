from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('registro', views.registro, name="registro"),
    path('inicioSesion/', views.inicioSesion, name="inicioSesion"),
    path('reset/password_reset', PasswordResetView.as_view(template_name='recuperacion/recuperarClave.html', email_template_name="recuperacion/correoRecuperarClave.html"), name = 'password_reset'),
    path('reset/password_reset_done', PasswordResetDoneView.as_view(template_name='recuperacion/recuperarClaveEstado.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='recuperacion/recuperarClaveFormulario.html'), name = 'password_reset_confirm'),
    path('reset/done',PasswordResetCompleteView.as_view(template_name='recuperacion/recuperarClaveCompletado.html'), name = 'password_reset_complete'),
]