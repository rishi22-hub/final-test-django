from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from functools import reduce
from operator import or_
from datetime import datetime
from django.db.models import Case, When, Value, CharField
from django.db.models import ExpressionWrapper, Func
from django.db.models.functions import TruncDate, Cast, Concat, ExtractDay,ExtractMonth,ExtractYear,Extract
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .forms import * 
# from .decorator import superuser_required,custom_permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission, ContentType
import csv
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request,"dashboard.html",{})

@login_required
def branch_table(request):
    return render(request,'list_branch.html',{})


@login_required
def branch_table_json(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]')
    order_column_index = int(request.GET.get('order[0][column]',default=-1))
    order_direction = request.GET.get('order[0][dir]')
    if search_value is None:
        search_value=""
    search_value = search_value.strip()
    search_value =search_value.lower()
    column_names = ['name', 'city']
    q_obj=reduce(or_ , (Q(**{i + '__icontains': search_value}) for i in column_names))
    q_obj |= Q(dealer_field__name=search_value)  
    data = Branch.objects.annotate(
    status_annotation=Case(
        When(is_active=True, then=Value('active')),
        When(is_active=False, then=Value('inactive')),
        output_field=CharField(),
    )

).filter(
    q_obj | Q(status_annotation__icontains=search_value)
)
   
    if order_column_index != -1:
        columns=column_names
        if order_column_index<len(columns):
            sort_field = columns[order_column_index]

            if order_direction == 'asc':
                data = data.order_by(sort_field)
            else:
                data = data.order_by(f'-{sort_field}')
    total_records = data.count()
    filtered_records = data.count()
    records = []
    for item in data[start:start+length]:
        manager_as_string=item.managers_as_string()
        records.append({
            'dealer': item.dealer_field.name,
            'name':item.name,
            'city': item.city,
            'managers': manager_as_string,
            'is_active': item.is_active,
            'id':item.id
       })
    
    for item in records:
        item["is_active"] = ["Active" if item["is_active"] else "Inactive"]
  
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": records,
    }
    
    return JsonResponse(response)


def add_branch(request):
    form = BranchForm(request.POST or None)
    if request.method == 'POST':
        form = BranchForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,"data added successfully")
            return redirect('list_branch')
        else:
            form = BranchForm()
        
    return render(request,"add_branch.html",{'form':form})




def edit_branch(request,id):
    branch = get_object_or_404(Branch, id=id)
    
    if request.method == 'POST':
        form = BranchForm(request.POST or None, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request,"data edited successfully")
            return redirect('list_branch') 
    else:
        form = BranchForm(instance=branch)
    
    return render(request, 'add_branch.html', {'form': form})



def show_products_in_branch(request,id):
    return render(request,'list_products.html',{'id':id})


def product_table_json(request,id):
    print(id)
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]')
    order_column_index = int(request.GET.get('order[0][column]',default=-1))
    order_direction = request.GET.get('order[0][dir]')
    if search_value is None:
        search_value=""
    search_value = search_value.strip()
    search_value =search_value.lower()
    column_names = ['name']
    q_obj=reduce(or_ , (Q(**{i + '__icontains': search_value}) for i in column_names))
    q_obj &= Q(branch_field_id=id) 
    data = Product.objects.filter(q_obj)
   
    if order_column_index != -1:
        columns=column_names
        if order_column_index<len(columns):
            sort_field = columns[order_column_index]

            if order_direction == 'asc':
                data = data.order_by(sort_field)
            else:
                data = data.order_by(f'-{sort_field}')
    total_records = data.count()
    filtered_records = data.count()
    records = []
    print(data)
    for item in data[start:start+length]:
        records.append({
            'branch': item.branch_field.name,
            'name':item.name,
            'quantity': item.quantity,
            'category':item.category,
            'unit_cost': item.unit_cost,
            'id':item.id
       })
    

  
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": records,
    }
    
    return JsonResponse(response)



def dealer_table(request):
    return render(request,'list_dealers.html')


def dealer_table_json(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]')
    order_column_index = int(request.GET.get('order[0][column]',default=-1))
    order_direction = request.GET.get('order[0][dir]')
    if search_value is None:
        search_value=""
    search_value = search_value.strip()
    search_value =search_value.lower()
    column_names = ['name', 'email']
    q_obj=reduce(or_ , (Q(**{i + '__icontains': search_value}) for i in column_names))
    data = Dealer.objects.annotate(
    status_annotation=Case(
        When(is_active=True, then=Value('active')),
        When(is_active=False, then=Value('inactive')),
        output_field=CharField(),
    )

).filter(
    (q_obj | Q(status_annotation__icontains=search_value))
)
   
    if order_column_index != -1:
        columns=column_names
        if order_column_index<len(columns):
            sort_field = columns[order_column_index]

            if order_direction == 'asc':
                data = data.order_by(sort_field)
            else:
                data = data.order_by(f'-{sort_field}')
    total_records = data.count()
    filtered_records = data.count()
    records = []
    for item in data[start:start+length]:
        records.append({
           
            'name':item.name,
            'email': item.email,
            'is_active':item.is_active,
            'id':item.id
       })
    

  
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": records,
    }
    
    return JsonResponse(response)



def show_branch_under_dealer(request,id):
    return render(request,'branch_under_dealer.html',{"id":id})

def show_branch_under_dealer_table_json(request,id):
    user=User.objects.get(id=id)
    dealer=Dealer.objects.get(user=user)
    id=dealer.id
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]')
    order_column_index = int(request.GET.get('order[0][column]',default=-1))
    order_direction = request.GET.get('order[0][dir]')
    if search_value is None:
        search_value=""
    search_value = search_value.strip()
    search_value =search_value.lower()
    column_names = ['name', 'city']
    q_obj=reduce(or_ , (Q(**{i + '__icontains': search_value}) for i in column_names))
    # q_obj |= Q(dealer_name_icontains=search_value) 
    print("id is ",id) 
    if user.role != "admin":
        q_obj &= Q(dealer_field_id=id)
    data = Branch.objects.annotate(
    status_annotation=Case(
        When(is_active=True, then=Value('active')),
        When(is_active=False, then=Value('inactive')),
        output_field=CharField(),
    )

).filter(
    (q_obj | Q(status_annotation__icontains=search_value))
)
   
    # data=data.filter(dealer_field_id=id)
    print("data is ",data)
    if order_column_index != -1:
        columns=column_names
        if order_column_index<len(columns):
            sort_field = columns[order_column_index]
            if order_direction == 'asc':
                data = data.order_by(sort_field)
            else:
                data = data.order_by(f'-{sort_field}')
    total_records = data.count()
    filtered_records = data.count()
    records = []

    # data=data[0].branches.all()
    print(data)
    for item in data[start:start+length]:
        print(item.dealer_field.id)
        manager_as_string=item.managers_as_string()
        records.append({
            'dealer': item.dealer_field.name,
            'name':item.name,
            'city': item.city,
            'managers': manager_as_string,
            'is_active': item.is_active,
            'id':item.id
       })
    
    for item in records:
        item["is_active"] = ["Active" if item["is_active"] else "Inactive"]
  
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": records,
    }
    
    return JsonResponse(response)

@login_required
def add_manager(request):
    form=ManagerForm(request.POST or None)
    if request.method == 'POST':
        form = ManagerForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,"data added successfully")
            return redirect('list_branch')
        else:
            form = ManagerForm()
        
    return render(request,"add_manager.html",{'form':form})


@login_required
def add_product(request):
    form=ProductForm(request.POST or None)
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,"data added successfully")
            return redirect('list_branch')
        else:
            form = ProductForm()
        
    return render(request,"add_product.html",{'form':form})





def add_to_cart(request, product_id):
    click_count = int(request.POST.get('quantity', 1))
    print(click_count)
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += click_count
    else:
        cart[str(product_id)] = {'quantity': click_count, 'price': str(product.unit_cost)}

    request.session['cart'] = cart
    return JsonResponse({'success':True})



def update_cart(request, product_id):
    # form=CartUpdateForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id]['quantity'] = quantity
    else:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    print(product_id)
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity']
        })
        cart_total += product.unit_cost * item_data['quantity']

    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})





def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})




def process_checkout(request):
    print(request.method)

    cart = request.session.get('cart', {})
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if product.quantity >= item_data['quantity']:
            product.quantity -= item_data['quantity']
            product.save()
            order = Order(
                product=product, 
                created_by=request.user,
                order_quantity=item_data['quantity']
            )
            order.save()
        else:
            raise ValidationError("Not enough stock to fulfill order")
    del request.session['cart']
    
    messages.success(request,"order placed successfully!!!")
    return redirect('dashboard')
     

