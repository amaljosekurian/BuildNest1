from pickle import ADDITEMS
from django import views
from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('', index, name="index"),
    path('signup/', signup, name='signup'),
    path('index2/', index2, name='index2'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', logout, name="logout"),
    path('adminreg/',adminreg,name="adminreg"),
    path('accounts/login/',user_login,name='login'), 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('toggle-active/<int:user_id>/<str:is_active>/',toggle_active, name='toggle_active'),
    path('contractor/', contractor, name='contractor'),
    path('construction_sites/', construction_sites, name='construction_sites'),
    path('client/', client, name='client'),
    path('purchase_manager/', purchase_manager, name='purchase_manager'),
    path('user_profile/', user_profile, name="user_profile"),
    path('update_user_details/', update_user_details, name="update_user_details"),
    path('sitereg/',sitereg,name="sitereg"),
    path('UserAcivation/<int:id>/', UserAcivation, name='UserAcivation'),
    path('requestContract/', requestContract, name='requestContract'),
    path('requestContract2/', requestContract2, name='requestContract2'),
    path('succesfullContract/', SuccessView, name='succesfullContract'),
    path('engineerIndex/', EngineerIndex, name='engineerIndex'),
    path('projectExplorer/<int:id>/', ProjectExplorer, name='projectExplorer'),
    path('createFeeToken/<int:id>/', createFeeToken, name='createFeeToken'),
    path('planBillPayment/<int:id>/', planBillPayment, name='planBillPayment'),
    path('successPage/', successPage, name='successPage'),
    path('projectplanUpdate/<int:id>/', projectplanUpdate, name='projectplanUpdate'),
    path('add_site/', add_site, name='add_site'),
    path('add_construction_site/', add_construction_site, name='add_construction_site'),
    path('add_worker/', add_worker, name='add_worker'),
    path('view_worker/', workers, name='view_worker'),
    path('', warehouse_home, name='warehouse_home'),
    path('add_product/', add_product, name='add_product'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('add_to_site/', add_to_site, name='add_to_site'),
    path('get_product_details/', get_product_details, name='get_product_details'),
    path('add-category/', add_category, name='add_category'),




    
    

    
    # Other URL patterns...
]

    # path('add_item_to_site/', add_item_to_site, name='add_item_to_site'),







    
    
    # path('delAdmin/', delAdmin, name='delAdmin')


