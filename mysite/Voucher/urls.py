from django.urls import path, re_path
from . import views



app_name = 'voucher'
urlpatterns = [
    path('', views.index, name='home'),
    re_path(r'^subject/create/', views.subject, name='subject-create'),
    re_path(r'^account/create/', views.account_create, name='account-create'),
    #path('subject/create/', views.SubjectCreate.as_view(), name='subject-create'),
    #path('subject/<int:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),
    path('subject/<int:pk>/', views.manage_subject, name='subject-detail'),
    #path('subject/detail/<int:pk>/', views.view_subject, name='subject-view'),
    #path('subject/', views.SubjectListView.as_view(), name='subject'),
    path('subject/', views.subjectList, name='subject-list'),
    path('account/', views.accountList, name='account-list'),
    re_path(r'^subject/filter/', views.subject_search, name='subject-filter'),
    re_path(r'^account/filter/', views.account_search, name='account-filter'),
]
