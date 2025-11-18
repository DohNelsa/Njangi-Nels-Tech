from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('', views.contribution_list, name='list'),
    path('create/', views.contribution_create, name='create'),
    path('account/<int:member_id>/', views.account_balance, name='account_balance'),
    path('yearly-statement/', views.yearly_statement, name='yearly_statement'),
    path('withdrawals/', views.withdrawal_list, name='withdrawal_list'),
    path('withdrawals/create/', views.withdrawal_create, name='withdrawal_create'),
    path('withdrawals/<int:pk>/approve/', views.withdrawal_approve, name='withdrawal_approve'),
    path('logs/', views.transaction_logs, name='transaction_logs'),
]


