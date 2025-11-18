from django.urls import path
from . import views
from . import reports

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('member/', views.member_dashboard, name='member'),
    path('admin/', views.admin_management, name='admin_management'),
    path('reports/contributions/', reports.export_contributions_report, name='export_contributions'),
    path('reports/members/', reports.export_members_report, name='export_members'),
    path('reports/transactions/', reports.export_transaction_logs, name='export_transactions'),
]

