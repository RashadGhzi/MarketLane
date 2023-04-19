from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('women/products/', views.WomenItemsView.as_view(), name='women_porducts'),
    path('men/products/', views.MenItemsView.as_view(), name="men_products"),
    path('product/view/<int:id>/', views.ProductView.as_view(), name='product_view'),
    path('product/category/<slug:data>/product/view/<int:id>/', views.ProductView.as_view(), name='product_view'),
    path('product/category/<slug:data>/', views.CatergoryView.as_view(), name='category_view'),
    path('category/men/product/', views.CategoryMenAjax.as_view(), name='category_product_men'),
    path('category/women/product/', views.CategoryWomenAjax.as_view(), name='category_product_women'),
    path('customer/address/', views.CustomerAddressLoc.as_view(), name='customer_address'),
    path('customer/address/del/<int:id>/', views.CustomerAddressDel.as_view(), name='customer_address_del'),
    path('product/cart/', views.ProductCartView.as_view(),name='product_cart'),
    path('add/product/cart/', views.AddProductCart.as_view(), name='add_product_cart'),
    path('remove/product/cart/<int:id>/', views.RemoveProductCart.as_view(), name='remove_product_cart'),
    path('plus/product/cart/', views.PlusProductCart.as_view(), name='plus_product_cart'),
    path('minus/product/cart/', views.MinusProductCart.as_view(), name='minus_product_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='check_out'),
    path('payment/done/', views.PaymentDone.as_view(), name='payment_done'),
    path('order/', views.OrderPlaced.as_view(), name='order'),
    path('prod/view/checkout/<int:id>/', views.ProductViewCheck.as_view(), name='prod_view_checkout'),
    path("prod/view/checkout/done/", views.ProductViewCheckDone.as_view(), name="prod_view_check_done")
]
