from django.urls import path, re_path
from . import views

app_name = 'entities'

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('our_instructors/', views.our_instructors_page, name='our_instructors'),
    path('instructor<int:pk>/', views.InstructorDetailsView.as_view(), name='instructor_details'),
    re_path(r'^services/$', views.services_page, name='services'),
    path('halls/', views.halls_page, name='halls'),
    re_path(r'^login/$', views.login_page, name='login'),
    re_path(r'^signin/$', views.signin_page, name='signin'),
    path('instructor/', views.instructor_page, name='instructor'),
    path('client_page/', views.client_page, name='client'),
    re_path(r'^user/$', views.user_page, name='user'),
    re_path(r'^logout/$', views.logout_page, name='logout'),
    re_path(r'^change/$', views.change_client_page, name='change_client'),
    path('group<int:id>/', views.client_group_page, name='group_details'),
    re_path(r'^groups/$', views.groups_page, name='groups'),
    path('groups/buy<int:id>', views.group_buy_page, name='group_buy'),
    re_path(r'^club_card/$', views.client_club_card_page, name='client_buy_card'),
    path('service_clients<int:id>/', views.service_clients_page, name='service_clients'),
    re_path(r'^change_instructor/$', views.change_instructor_page, name='change_instructor'),
    path('su/', views.superuser_page, name='superuser'),
    re_path(r'^about/$', views.about_page, name='about'),
    re_path(r'^company/$', views.company_info_page, name='company'),
    re_path(r'^news/$', views.news_page, name='news'),
    re_path(r'^empl/$', views.employees_page, name='employees'),
    re_path(r'^coupons/$', views.coupons_page, name='coupons'),
    re_path(r'^faq/$', views.faq_page, name='faq'),
    re_path(r'^reviews/$', views.reviews_page, name='reviews'),
    re_path(r'^vacancies/$', views.vacancies_page, name='vacancies'),
    re_path(r'^review/$', views.create_review_page, name='create_review'),
    re_path(r'^age_chart/$', views.age_chart, name='age_chart'),
    re_path(r'^workout_chart/$', views.service_chart, name='service_chart'),
    re_path(r'^age_distrib/$', views.age_distrib, name='age_distrib'),
    re_path(r'^service_distrib/$', views.service_distrib, name='service_distrib'),
    

    re_path(r'^deletemy/$', views.chose, name='delinst'),
    re_path(r'^createinst/$', views.crinst, name='createinst'),

    path(r'^del_sel<int:id>/$', views.delete_selected, name='del_sel'),

    
    
]
