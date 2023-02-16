from django.urls import path
from . import views



app_name = 'feeds'

urlpatterns = [
    # User Login/Logout, Registration, & profile settings urls
    path('registration/',views.register,name='register'),
    path('password/', views.change_password, name='password'),
    path('password-success/', views.password_success,name='password_success'),
    path('edit_profile/',views.UserEditView.as_view(),name='edit_profile'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    # Feed Log urls
    path('feedlog/',views.feed_log_view,name='feedlog'),
    path('delete/<int:formulalog_id>/',views.feed_log_delete,name='delete'),

    #Chart data urls
    path('dailydata/',views.daily_data),
    path('monthdata/',views.monthly_data),
    path('weeklydata/', views.weekly_data),

    # Weight data urls
    path('weightlog/', views.weight_log, name='weightlog'),
    path('weightdelete/<int:weight_id>/',views.weight_log_delete,name='weightdelete'),
]