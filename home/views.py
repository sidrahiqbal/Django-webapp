import json

import stripe
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth import get_user, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import ProductForm, JsonForm, UserForm
from .models import Order, Product
from .utils import handle_uploaded_file
from django.conf import settings


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_url = 'shop'
    success_message = 'You are successfully logged in'


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Your account has been created. You can log in now!')
        return super().form_valid(form)


class ShopProducts(ListView):

    context_object_name = 'products'
    queryset = Product.objects.all()[:9]
    template_name = 'shop.html'


class CategoryProducts(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'category_specific.html'

    def post(self, request, category, gender):
        request.session['filtered_products_ids'] = [product.product_id for product in Product.objects.filter(
                                                    category__contains=category).filter(gender__contains=gender).filter(
                                                    price__range=(request.POST.get('min'), request.POST.get('max')))]
        request.session['url'] = request.get_full_path()

        return redirect('filter_products')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(category__contains=self.kwargs['category']).filter(gender__contains=self.kwargs['gender'])
        paginator = Paginator(queryset, 21)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj


class FilterProducts(ListView):
    modal = Product
    context_object_name = 'products'
    template_name = 'filtered.html'

    def get_queryset(self):
        queryset = Product.objects.filter(product_id__in=self.request.session['filtered_products_ids'])
        paginator = Paginator(queryset, 21)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj


class SearchBrand(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'brand.html'

    def post(self, request):
        brand = self.request.POST.get('brand')
        request.session['brand_products_ids'] = [product.product_id for product in Product.objects.filter
                                                 (brand__contains=brand)]

        return redirect('/search_brand/')

    def get_queryset(self):
        brand_products = Product.objects.filter(product_id__in=self.request.session['brand_products_ids'])
        paginator = Paginator(brand_products, 21)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj


@method_decorator(login_required, name='post')
class ResetPassword(FormView):
    template_name = 'password_reset.html'

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            return redirect('/')

        messages.error(request, 'Please correct the error below.')

        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = PasswordChangeForm(request.user)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='get')
class DeleteAccount(View):

    def get(self, request):
        user = get_user(request)
        user.delete()
        messages.success(request, 'Account Deleted')

        return redirect("/login")


class AddProduct(SuccessMessageMixin, CreateView):
    template_name = 'add_product.html'
    form_class = ProductForm
    success_url = '/'
    success_message = 'Product successfully added!'


class AddJsonFile(View):
    @method_decorator(login_required)
    def post(self, request):
        form = JsonForm(request.POST, request.FILES)
        if form.is_valid():
            file = open(handle_uploaded_file(self.request.FILES["jsonfile"]))
            products_json = json.load(file)

            for product in products_json:
                new_product = Product(title=product['name'],
                                      brand=product['brand'],
                                      gender=product['gender'],
                                      category=product['category'],
                                      price=product['price'],
                                      description=product['description'],
                                      care=product['care'],
                                      size=product['size'],
                                      color=product['color'],
                                      image_urls=product['image_urls'])
                new_product.save()

        messages.success(self.request, f'Products successfully added!')

        return redirect('/')

    def get(self, request):
        return render(request, 'json.html', {'form': JsonForm()})


@method_decorator(login_required, name='post')
class DeleteProduct(View):

    def get(self, request, id):
        product = Product.objects.get(product_id=id)
        context = {'product': product.title}

        return render(request, 'delete_product.html', context)

    def post(self, request, id):
        product = Product.objects.get(product_id=id)
        product.delete()
        messages.success(request, 'Product deleted')

        return redirect('/')


@method_decorator(login_required, name='post')
class UpdateProduct(UpdateView):
    modal = Product
    template_name = 'update_product.html'
    form_class = ProductForm

    def get_object(self):
        return Product.objects.get(product_id=self.kwargs['id'])

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated')

            return redirect('/')

        return render(request, self.template_name, {'form': form})


class ViewProduct(DetailView):

    def get(self, request, id):
        product = Product.objects.get(product_id=id)
        context = {'image_urls': product.image_urls, 'title': product.title, 'id': product.product_id,
                   'gender': product.gender, 'brand': product.brand, 'category': product.category,
                   'price': product.price, 'description': product.description, 'care': product.care,
                   'size': product.size, 'color': product.color}

        return render(request, 'view_product.html', context)


class PlaceOrder(View):

    @method_decorator(login_required)
    def post(self, request, id):
        product = Product.objects.get(product_id=id)
        quantity = int(request.POST.get('quantity'))
        size = request.POST.get('size')
        color = request.POST.get('color')
        existing_order = Order.objects.filter(product_id=id, username=request.user.id, size=size, color=color)
        if existing_order:
            existing_order.update(quantity=quantity+existing_order.values()[0]['quantity'])
        else:
            Order.objects.create(username=request.user, product_id=product, quantity=quantity, size=size, color=color)
        messages.success(request, 'Product added to cart')

        return redirect('shop')


@method_decorator(login_required, name='get')
class Cart(View):
    def get(self, request):
        orders = Order.objects.filter(username=request.user.id)
        orders_in_cart = []

        for order in orders:
            if order.status == 'unpaid':
                orders_in_cart.append({'product_name': getattr(Product.objects.get(product_id=order.product_id), 'title'),
                                       'product_price': getattr(Product.objects.get(product_id=order.product_id),'price'),
                                       'total': order.quantity * getattr(Product.objects.get(product_id=order.product_id), 'price'),
                                       'image': getattr(Product.objects.get(product_id=order.product_id), 'image_urls'),
                                       'quantity': order.quantity, 'order_id': order.order_id, 'size': order.size,
                                       'color': order.color})
        request.session['unpaid_orders'] = orders_in_cart
        context = {'orders': orders_in_cart, 'total_amount': sum(order['total'] for order in orders_in_cart)}

        return render(request, 'cart.html', context=context)


@method_decorator(login_required, name='get')
class DeleteOrder(View):

    def get(self, request, id):
        order = Order.objects.get(order_id=id)
        order.delete()
        messages.success(request, 'Order deleted')

        return redirect('/cart')


class Success(View):

    def get(self, request):
        Order.objects.filter(order_id__in=[order['order_id'] for order in request.session[
            'unpaid_orders']]).update(status='paid')
        email = request.user.email
        send_mail(
            'Order Confirmed',
            'Hi! Thank you for trusting us. Your order is confirmed and will be delivered soon',
            'candida@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Order confirmation email sent')

        return redirect('/')


class Failure(View):

    def get(self, request):
        messages.warning(request, 'Payment failed! checkout again')
        return redirect('/cart')


@method_decorator(login_required, name='get')
class Checkout(View):

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': order['product_name'],
                    },
                    'unit_amount': order['product_price'] * 100,
                },
                'quantity': order['quantity']
            } for order in request.session['unpaid_orders']],
            customer_email=request.user.email,
            mode='payment',
            success_url='http://127.0.0.1:8000' + '/success/',
            cancel_url='http://127.0.0.1:8000' + '/failure',
        )

        return redirect(checkout_session.url)
