from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mandir'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('notices/', views.notice_list, name='notices'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('committee/', views.committee_list, name='committee'),
    path('contact/', views.contact, name='contact'),

    # Authentication ko lagi
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # admin ko dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # admin ko section
    path('manage/events/', views.admin_event_list, name='admin_event_list'),
    path('manage/events/create/', views.event_create, name='event_create'),
    path('manage/events/<int:pk>/update/', views.event_update, name='event_update'),
    path('manage/events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('manage/events/<int:pk>/images/<int:image_pk>/delete/', 
         views.event_image_delete, name='event_image_delete'),

    path('manage/notices/', views.admin_notice_list, name='admin_notice_list'),
    path('manage/notices/create/', views.notice_create, name='notice_create'),
    path('manage/notices/<int:pk>/update/', views.notice_update, name='notice_update'),
    path('manage/notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),

    path('manage/blog/', views.admin_blog_list, name='admin_blog_list'),
    path('manage/blog/create/', views.blog_create, name='blog_create'),
    path('manage/blog/<int:pk>/update/', views.blog_update, name='blog_update'),
    path('manage/blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    path('manage/committee/', views.admin_committee_list, name='admin_committee_list'),
    path('manage/committee/create/', views.committee_create, name='committee_create'),
    path('manage/committee/<int:pk>/update/', views.committee_update, name='committee_update'),
    path('manage/committee/<int:pk>/delete/', views.committee_delete, name='committee_delete'),
    path('manage/committee/<int:committee_pk>/members/create/', 
         views.committee_member_create, name='committee_member_create'),
    path('manage/committee/members/<int:pk>/update/', 
         views.committee_member_update, name='committee_member_update'),
    path('manage/committee/members/<int:pk>/delete/', 
         views.committee_member_delete, name='committee_member_delete'),

    path('manage/donors/', views.admin_donor_list, name='admin_donor_list'),
    path('manage/donors/create/', views.donor_create, name='donor_create'),
    path('manage/donors/<int:pk>/update/', views.donor_update, name='donor_update'),
    path('manage/donors/<int:pk>/delete/', views.donor_delete, name='donor_delete'),

    path('manage/contacts/', views.admin_contact_list, name='admin_contact_list'),
    path('manage/contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('manage/contacts/<int:pk>/toggle-read/', 
         views.contact_toggle_read, name='contact_toggle_read'),
    path('manage/contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),

    path('gallery/', views.gallery_view, name='gallery'),
    path('about/', views.about_view, name='about'),
    path('manage/about/', views.admin_about_list, name='admin_about_list'),
    path('manage/about/create/', views.about_create, name='about_create'),
    path('manage/about/<int:pk>/update/', views.about_update, name='about_update'),
    path('manage/about/<int:pk>/delete/', views.about_delete, name='about_delete'),

    path('mission-vision/', views.mission_vision_view, name='mission_vision'),
    path('manage/mission-vision/', views.admin_mission_vision_list, name='admin_mission_vision_list'),
    path('manage/mission-vision/create/', views.mission_vision_create, name='mission_vision_create'),
    path('manage/mission-vision/<int:pk>/update/', views.mission_vision_update, name='mission_vision_update'),
    path('manage/mission-vision/<int:pk>/delete/', views.mission_vision_delete, name='mission_vision_delete'),

    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
] 