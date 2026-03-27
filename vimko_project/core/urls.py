
# from rest_framework.routers import DefaultRouter


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('products/', views.ProductListCreateView.as_view()),
#     path('products/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view()),

#     path('dealers/', views.DealerListCreateView.as_view()),
#     path('dealers/<int:pk>/', views.DealerRetrieveUpdateView.as_view()),

#     path('inventory/', views.InventoryListView.as_view()),
#     path('inventory/<int:product_id>/', views.InventoryUpdateView.as_view()),
#     path('inventory/add/', views.InventoryCreateView.as_view()),   # POST create
#     path('orders/', views.OrderListCreateView.as_view()),
#     path('orders/<int:pk>/', views.OrderRetrieveUpdateView.as_view()),
#     path('orders/<int:pk>/confirm/', views.OrderConfirmView.as_view()),
#     path('orders/<int:pk>/deliver/', views.OrderDeliverView.as_view()),
   
# ]


from django.urls import path
from . import views

urlpatterns = [
    # ====== FRONTEND TEMPLATE PAGES ======
    path('', views.home, name='home'),

    # Products (Template)
    path('products-ui/', views.product_list, name='product_list'),
    path('products-ui/create/', views.product_create, name='product_create'),
    path('products-ui/<int:pk>/update/', views.product_update, name='product_update'),
    path('products-ui/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Dealers (Template)
    path('dealers-ui/', views.dealer_list, name='dealer_list'),
    path('dealers-ui/create/', views.dealer_create, name='dealer_create'),
    path('dealers-ui/<int:pk>/update/', views.dealer_update, name='dealer_update'),

    # Inventory (Template)
    path('inventory-ui/', views.inventory_list, name='inventory_list'),
    path('inventory-ui/add/', views.inventory_create, name='inventory_create'),
    path('inventory-ui/<int:product_id>/update/', views.inventory_update, name='inventory_update'),

    # Orders (Template)
    path('orders-ui/', views.order_list, name='order_list'),
    path('orders-ui/create/', views.order_create, name='order_create'),
    # path('orders-ui/detail/',views.order_detail,name='order_detail'),
    path('orders-ui/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders-ui/<int:pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('orders-ui/<int:pk>/deliver/', views.order_deliver, name='order_deliver'),

    # ====== BACKEND API ENDPOINTS (REST Framework) ======
    path('products/', views.ProductListCreateView.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view()),

    path('dealers/', views.DealerListCreateView.as_view()),
    path('dealers/<int:pk>/', views.DealerRetrieveUpdateView.as_view()),

    path('inventory/', views.InventoryListView.as_view()),
    path('inventory/<int:product_id>/', views.InventoryUpdateView.as_view()),
    path('inventory/add/', views.InventoryCreateView.as_view()),   # POST create

    path('orders/', views.OrderListCreateView.as_view()),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateView.as_view()),
    path('orders/<int:pk>/confirm/', views.OrderConfirmView.as_view()),
    path('orders/<int:pk>/deliver/', views.OrderDeliverView.as_view()),
]

