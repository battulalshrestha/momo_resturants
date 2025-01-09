from django.urls import path
from .views import index,contact,about,menu,services,register,log_in
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("menu/", menu, name="menu"),
    path("services/", services, name="services"),
    path('register/',register,name = "register"),
    path('login/',log_in,name = "login"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
      path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done')

]

# urlpatterns += [
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]
