from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='front'),
    path('admi_login/',views.admi_login,name='admi_login'),
    path('resort/register', views.resort_reg, name='resort_reg'),
    path('resort-list/', views.resort_list, name='resort_list'),
   path('edit-resort/<str:name>/', views.edit_resort, name='edit_resort'),
    path('delete-resort/<str:name>/', views.resort_delete, name='delete_resort'),
    path('add_room/', views.add, name='add_room'), 
    path('room/register/<str:resort_name>/', views.room_reg, name='room_reg'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/edit/<int:room_id>/', views.room_update, name='edit_room'),
    path('room/delete/<int:room_id>/', views.room_delete, name='delete_room'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('check_avilable/', views.check_avilable, name='check_avilable'),
    path('get-resorts/', views.get_resorts, name='get_resorts'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    
   path('card-transaction/<int:booking_id>/', views.card_transaction, name='card_transaction'),
    path('users/', views.user_list_view, name='user_list'),
     path('booking-info/<int:booking_id>/', views.booking_info_view, name='booking-info'),
   #path('booking-info/', views.booking_info_view, name='booking_info'),
    path('manage-users/', views.manage_users, name='manage_users'), 
   
    path('manage-booking/', views.manage_booking, name='manage_booking'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
