from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, FormView, UpdateView
from .models import Product, CustomerAddress, ProductCart, Order
from django.http import JsonResponse
from .forms import CustomerAddressForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(ListView):
    template_name = 'core/home.html'
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_cloth"] = Product.objects.filter(category='CL').order_by('id')[:10]
        context["products_shoes"] = Product.objects.filter(category='SH').order_by('id')[:10]
        context["products_sunglass"] = Product.objects.filter(category='SG').order_by('id')[:10]
        return context

class WomenItemsView(ListView):
    template_name = 'core/women_item.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["women_products"] = Product.objects.filter(gender='F').order_by('?')
        return context

class MenItemsView(ListView):
    template_name = 'core/men_item.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["men_products"] = Product.objects.filter(gender='M').order_by('?')
        return context

class ProductView(View):
    def get(self, request, id, *args, **kwargs):
        product_obj = Product.objects.get(id=id)
        context = {
            "product_obj":product_obj
        }
        return render(request, 'core/product_view.html', context)

my_dict = {}
class CatergoryView(View):
    def get(self, request, data, *args, **kwargs):
        if data == 'cloth':
            prod_obj = Product.objects.filter(category='CL')
            my_dict['pro_cat']='CL'
        elif data == 'shoes':
            prod_obj = Product.objects.filter(category='SH')
            my_dict['pro_cat']='SH'
        elif data == 'sunglass': 
            prod_obj = Product.objects.filter(category='SG')
            my_dict['pro_cat']='SG'
        context = {
            'data':prod_obj
        }
        return render(request, 'core/category_view.html', context)

class CategoryMenAjax(View):
    def get(self, request, *args, **kwargs):
        image_url_list = []
        # print(my_dict)
        prod_cat = my_dict['pro_cat']
        cat_gen_prod = Product.objects.filter(category=prod_cat).filter(gender='M').values()
        list_prod = list(cat_gen_prod)

        obj_list = Product.objects.filter(category=prod_cat).filter(gender='M').values('id')
        # print(obj_list)
        for i in obj_list:
            id = i['id']
            id_obj = Product.objects.get(pk=id)
            img_path = id_obj.product_image.url
            print(img_path)
            image_url_list.append(img_path)
        
        # print(image_url_list)


        context = {'cat_gen_prod':list_prod, 'image_url_list':image_url_list}
        return JsonResponse(context)
    

class CategoryWomenAjax(View):
    def get(self, request, *args, **kwargs):
        image_url_list = []
        # print(my_dict)
        prod_cat = my_dict['pro_cat']
        cat_gen_prod = Product.objects.filter(category=prod_cat).filter(gender='F').values()
        list_prod = list(cat_gen_prod)

        obj_list = Product.objects.filter(category=prod_cat).filter(gender='F').values('id')
        # print(obj_list)
        for i in obj_list:
            id = i['id']
            id_obj = Product.objects.get(pk=id)
            img_path = id_obj.product_image.url
            print(img_path)
            image_url_list.append(img_path)
        
        # print(image_url_list)
        context = {'cat_gen_prod':list_prod, 'image_url_list':image_url_list}
        return JsonResponse(context)
    

class CustomerAddressLoc(LoginRequiredMixin,FormView, ListView):
    login_url = reverse_lazy('user_login')
    form_class = CustomerAddressForm
    template_name = 'core/customer_profile.html'
    model = CustomerAddress
    success_url = reverse_lazy('customer_address')

    def form_valid(self, form) :
        customer_name = self.request.user
        form.instance.customer = customer_name
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cus_loc_objects"] = CustomerAddress.objects.filter(customer=self.request.user).order_by('-id')
        return context

class CustomerAddressDel(View):
    def dispatch(self, request, id, *args, **kwargs):
        cus_add = CustomerAddress.objects.filter(id=id)
        cus_add.delete()   
        return redirect('customer_address')
    


# other time not important
# class CustomerAddressUpdate(View):
#     def get(self, request, id, *args, **kwargs):
#         print(id)
#         cus_add = CustomerAddress.objects.filter(id=id).values()
#         cus_data = list(cus_add)
#         # print(address_form)
#         return JsonResponse({'data':cus_data})

# showing added product cart 
class ProductCartView(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        cart_products = ProductCart.objects.filter(user=request.user).order_by('-id')
        products_total_price = 0.0

        if cart_products:
            for cart in cart_products:
                products_total_price += cart.get_total_cost()
            products_total_price_with_shipping_cost = products_total_price + 70
            context = {
                'cart_products':cart_products,
                'products_total_price':products_total_price,
                'products_total_price_with_shipping_cost':products_total_price_with_shipping_cost
            }
            return render(request, 'core/product_cart.html', context)
        else:
            return render(request, 'core/no_cart.html')

# adding product to ProductCart model database using ajax 
class AddProductCart(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        user = self.request.user
        # print(user)
        prod_id = self.request.GET.get('prod_id')
        # print(prod_id)
        prod_obj = Product.objects.get(id=prod_id)
        ProductCart(user=user, product=prod_obj).save()
        return JsonResponse({'response':True})

class RemoveProductCart(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, id, *args, **kwargs):
        cart_prod = ProductCart.objects.get(id=id)
        cart_prod.delete()
        return redirect('product_cart')

# cart quantity increase function   
class PlusProductCart(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        cart_id = request.GET['cart_id']
        print(cart_id)
        cart_obj = ProductCart.objects.get(id=cart_id)

        # quantity update 
        cart_obj.quantity += 1
        cart_obj.save()
        obj_total_price = cart_obj.get_total_cost()

        # getting current user cart objects
        cart_specific_obj = ProductCart.objects.filter(user=request.user)
        products_total_price = 0.0
        for obj in cart_specific_obj:
            products_total_price = products_total_price + obj.get_total_cost()

        products_total_price_with_shipping_price = products_total_price + 70
        context = {
            'cart_quantity':cart_obj.quantity,
            'obj_total_price':obj_total_price,
            'products_total_price':products_total_price,
            'products_total_price_with_shipping_price':products_total_price_with_shipping_price,
        }
        return JsonResponse(context)
    
# cart quantity decrease function   
class MinusProductCart(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        cart_id = request.GET['cart_id']
        print(cart_id)
        cart_obj = ProductCart.objects.get(id=cart_id)

        # quantity update 
        if cart_obj.quantity <= 1:
            cart_obj.quantity = 1
            cart_obj.save()
        else:
            cart_obj.quantity -= 1
        cart_obj.save()
        obj_total_price = cart_obj.get_total_cost()

        # getting current user cart objects
        cart_specific_obj = ProductCart.objects.filter(user=request.user)
        products_total_price = 0.0
        for obj in cart_specific_obj:
            products_total_price = products_total_price + obj.get_total_cost()

        products_total_price_with_shipping_price = products_total_price + 70
        context = {
            'cart_quantity':cart_obj.quantity,
            'obj_total_price':obj_total_price,
            'products_total_price':products_total_price,
            'products_total_price_with_shipping_price':products_total_price_with_shipping_price,
        }
        return JsonResponse(context)


class CheckoutView(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        carts = ProductCart.objects.filter(user=request.user).order_by('-id')
        address = CustomerAddress.objects.filter(customer=request.user).order_by('-id')
        products_total_price = 0.0
        for obj in carts:
            products_total_price = products_total_price + obj.get_total_cost()

        products_total_price_with_shipping_price = products_total_price+70
        context = {
            'carts':carts,
            'address':address,
            'products_total_price':products_total_price,
            'products_total_price_with_shipping_price':products_total_price_with_shipping_price,
        }
        return render(request, 'core/check_out.html', context)
    

class PaymentDone(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        add_id = self.request.GET.get('add_id')
        print(add_id)
        user = request.user
        product_cart = ProductCart.objects.filter(user=user)
        customer_loc = CustomerAddress.objects.get(id=add_id)
        for item in product_cart:
            Order(user=user, customer_loc=customer_loc, product=item.product, quantity=item.quantity).save()
            item.delete()
        return redirect('order')
    
class OrderPlaced(LoginRequiredMixin,View):
    login_url = reverse_lazy('user_login')
    def get(self, request, *args, **kwargs):
        return render(request, 'core/order.html')