from django.urls import path
from django.contrib.auth import views as auth_views

from home import views


urlpatterns = [
    path('', views.ShopProducts.as_view(), name='shop'),

    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('order/<int:id>', views.PlaceOrder.as_view(), name='order'),
    path('delete_order/<int:id>', views.DeleteOrder.as_view(), name='delete_order'),
    path('cart/', views.Cart.as_view(), name='cart'),

    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('success/', views.Success.as_view(), name='success'),
    path('failure/', views.Failure.as_view(), name='failure'),

    path('reset_password/', views.ResetPassword.as_view(), name='reset_password'),
    path('delete_account/', views.DeleteAccount.as_view(), name='delete_account'),

    path('filter_products/', views.FilterProducts.as_view(), name='filter_products'),
    path('search_brand/', views.SearchBrand.as_view(), name='search_brand'),
    path('categorywise_products/<str:category>/<str:gender>', views.CategoryProducts.as_view(), name='categorywise_products'),

    path('add_product/', views.AddProduct.as_view(), name= 'add_product'),
    path('add_json_file/', views.AddJsonFile.as_view(), name='add_json_file'),
    path('delete_product/<int:id>', views.DeleteProduct.as_view(), name='delete_product'),
    path('update_product/<int:id>', views.UpdateProduct.as_view(), name='update_product'),
    path('view_product/<int:id>', views.ViewProduct.as_view(), name='view_product'),
]
