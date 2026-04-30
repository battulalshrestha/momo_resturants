from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import PasswordResetView
urlpatterns = [
    # ── Core pages ──────────────────────────────────────────────
    path('',          views.index,    name='index'),
    path('menu/',     views.menu,     name='menu'),
    path('services/', views.services, name='services'),
    path('about/',    views.about,    name='about'),
    path('contact/',  views.contact,  name='contact'),
    path('profile/',  views.profile,  name='profile'),
    path('reservation/', views.reservation, name='reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # ── Auth ────────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/',    views.log_in,   name='login'),
    path('logout/',   views.log_out,  name='logout'),

    # ── Password Reset (Django built-ins) ───────────────────────
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='auth/password_reset.html',
             email_template_name='auth/password_reset_email.html',
             subject_template_name='auth/password_reset_subject.txt',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html',
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html',
         ),
         name='password_reset_complete'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='auth/password_reset.html',
             email_template_name='auth/password_reset_email.html',
             subject_template_name='auth/password_reset_subject.txt',
         ),
         name='password_reset'),

    # ── Cart ────────────────────────────────────────────────────
    path('cart/',                          views.cart_view,     name='cart'),
    path('cart/add/<int:item_id>/',        views.add_to_cart,   name='add_to_cart'),
    path('cart/remove/<int:item_id>/',     views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/',     views.update_cart,   name='update_cart'),

    # ── Orders ──────────────────────────────────────────────────
    path('order/place/',   views.place_order,   name='place_order'),
    path('order/history/', views.order_history, name='order_history'),

    # ── Reviews ─────────────────────────────────────────────────
    path('review/add/', views.add_review, name='add_review'),
     path('cart/', views.cart, name='cart'),
]