from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_list, name='list'),
    path('<int:pk>/', views.loan_detail, name='detail'),
    path('create/', views.loan_create, name='create'),
    path('<int:pk>/approve/', views.loan_approve, name='approve'),
    path('repayment/create/', views.repayment_create, name='repayment_create'),
    path('repayment/create/<int:loan_id>/', views.repayment_create, name='repayment_create_loan'),
]


