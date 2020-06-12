from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from .models import *
from .utils import cookie_cart, cart_data
import json


# Create your views here.

class IndexView(View):
    def get(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']
        a = SanPhamModel.objects.all()
        c = LoaiSPModel.objects.all()
        context = {
            'f': a,
            'danhmuc': c,
            'cart_items': cart_items,
        }
        return render(request, 'home/index.html', context)


def loaisp(request, id):
    data = cart_data(request)
    cart_items = data['cart_items']
    c = LoaiSPModel.objects.all()
    chitietsp = SanPhamModel.objects.all().filter(Loai_sp_id=id)
    return render(request, 'home/shop.html', {'f': chitietsp, 'danhmuc': c,'cart_items': cart_items,})


def chitiet(request, id):
    data = cart_data(request)
    cart_items = data['cart_items']
    c = LoaiSPModel.objects.all()
    chitietsp = SanPhamModel.objects.all().filter(id=id)
    return render(request, 'home/product-single.html', {'f': chitietsp, 'danhmuc': c,'cart_items': cart_items,})


def cart(request):
    c = LoaiSPModel.objects.all()
    data = cookie_cart(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
        'danhmuc': c
    }
    return render(request, 'home/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)
    return JsonResponse('Item was added', safe=False)


class Checkout(View):

    def get(self, request):
        c = LoaiSPModel.objects.all()
        data = cart_data(request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        context = {
            'items': items,
            'order': order,
            'cart_items': cart_items,
            'danhmuc': c
        }
        return render(request, 'home/checkout.html', context)
    def post(self, request):
        o = Order(request.POST)
        if o.is_valid():
            o.save()
            return HttpResponse('Lưu oke')
        else:
            return HttpResponse('Không lưu được')
