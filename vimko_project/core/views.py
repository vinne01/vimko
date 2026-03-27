from django.contrib import messages
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required

from django.forms import modelformset_factory
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import Product, Inventory, Dealer, Order, OrderItem
from .serializers import ProductSerializer, InventorySerializer, DealerSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser

# Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Dealers
class DealerListCreateView(generics.ListCreateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

class DealerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

# Inventory
class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
# Inventory Create
class InventoryCreateView(generics.CreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer    

# class InventoryUpdateView(generics.UpdateAPIView):
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer
#     lookup_field = 'product_id'
class InventoryUpdateView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'product_id'

    permission_classes = [IsAdminUser]  # 🔥 Only admin can update

    def get_object(self):
        product_id = self.kwargs['product_id']
        return Inventory.objects.get(product_id=product_id)

# Orders
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Confirm Order
class OrderConfirmView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, pk):
        order = self.get_object()
        if order.status != 'Draft':
            return Response({"error": "Only draft orders can be confirmed."}, status=400)
        insufficient = []
        for item in order.items.all():
            if item.product.inventory.quantity < item.quantity:
                insufficient.append({
                    "product": item.product.name,
                    "available": item.product.inventory.quantity,
                    "requested": item.quantity
                })
        if insufficient:
            return Response({"error": "Insufficient stock", "details": insufficient}, status=400)
        # Deduct stock
        for item in order.items.all():
            item.product.inventory.quantity -= item.quantity
            item.product.inventory.save()
        order.status = 'Confirmed'
        order.save()
        return Response({"message": "Order confirmed successfully."})

# Deliver Order
class OrderDeliverView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, pk):
        order = self.get_object()
        if order.status != 'Confirmed':
            return Response({"error": "Only confirmed orders can be delivered."}, status=400)
        order.status = 'Delivered'
        order.save()
        return Response({"message": "Order delivered successfully."})
    
    
    
# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Dealer, Inventory, Order, OrderItem
from .forms import OrderItemForm, ProductForm, DealerForm, InventoryForm, OrderForm

def home(request):
    return render(request, 'core/home.html')

# Products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'core/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'core/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

# Dealers
def dealer_list(request):
    dealers = Dealer.objects.all()
    return render(request, 'core/dealer_list.html', {'dealers': dealers})

def dealer_create(request):
    form = DealerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dealer_list')
    return render(request, 'core/dealer_form.html', {'form': form})

def dealer_update(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    form = DealerForm(request.POST or None, instance=dealer)
    if form.is_valid():
        form.save()
        return redirect('dealer_list')
    return render(request, 'core/dealer_form.html', {'form': form})

# Inventory

def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'core/inventory_list.html', {'inventory': inventory})
@staff_member_required
def inventory_create(request):
    form = InventoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventory_list')
    return render(request, 'core/inventory_form.html', {'form': form})
@staff_member_required
def inventory_update(request, product_id):
    inventory = get_object_or_404(Inventory, product_id=product_id)
    form = InventoryForm(request.POST or None, instance=inventory)
    if form.is_valid():
        form.save()
        return redirect('inventory_list')
    return render(request, 'core/inventory_form.html', {'form': form})

# Orders
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'core/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'core/order_detail.html', {'order': order}) 


def order_create(request):
    OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1, can_delete=True)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, queryset=OrderItem.objects.none())
        if order_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.status = 'Draft'
                order.save()
                total_amount = 0
                for item_form in formset:
                    if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                        product = item_form.cleaned_data['product']
                        qty = item_form.cleaned_data['quantity']
                        # Stock check
                        if product.inventory.quantity < qty:
                            messages.error(request, f"Insufficient stock for {product.name}. Available: {product.inventory.quantity}")
                            # raise transaction.TransactionManagementError
                            return render(request,'core/order_form.html',{
                                'order_form':order_form,
                                'formset':formset
                            })
                        item = OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=qty,
                            unit_price=product.price,
                            # line_total=Decimal(product.price) * Decimal(qty)
                        )
                        total_amount += item.line_total
                        # Deduct inventory
                        product.inventory.quantity -= qty
                        product.inventory.save()
                order.total_amount = total_amount
                order.save()
                messages.success(request, 'Order created successfully.')
                return redirect('order_list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())
    return render(request, 'core/order_form.html', {'order_form': order_form, 'formset': formset})

def order_confirm(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'Draft':
        messages.error(request, "Only draft orders can be confirmed.")
    else:
        order.status = 'Confirmed'
        order.save()
        messages.success(request, "Order confirmed successfully.")
    return redirect('order_list')

def order_deliver(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'Confirmed':
        messages.error(request, "Only confirmed orders can be delivered.")
    else:
        order.status = 'Delivered'
        order.save()
        messages.success(request, "Order delivered successfully.")
    return redirect('order_list')   
    
    


