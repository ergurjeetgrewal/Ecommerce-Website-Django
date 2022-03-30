from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order,OrderUpdate
from math import ceil
from datetime import date
import json
#csrf except handle
from django.views.decorators.csrf import csrf_exempt
#paytm
from paytm import Checksum
MERCHANT_KEY = 'tjJ#mBQKHBpeAi9m';
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def searchmatch(query,item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower() or query.lower() in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search','')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query,item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds,'msg':""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':'Please make sure to enter relevant keywords to get item displayed'}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        submit = True
        return render(request, 'shop/contact.html',{'submit':submit})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderid=request.POST.get('orderid','')
        email=request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates= []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_JSON],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse("{}")
    return render(request,'shop/tracker.html')


def productView(request, proid):
    product = Product.objects.filter(product_id=proid)
    print(product)
    return render(request, 'shop/productview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_JSON = request.POST.get('items_JSON', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        add1 = request.POST.get('add1', '')
        add2 = request.POST.get('add2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        orders = Order(items_JSON=items_JSON, name=name, email=email, phone=phone,
                       add1=add1, add2=add2, city=city, state=state, zip_code=zip_code,amount=amount)
        orders.save()
        update= OrderUpdate(order_id=orders.order_id,update_desc="Order Placed",timestamp=date)
        update.save()
        thank = True
        id = orders.order_id
        # return render(request, 'shop/checkout.html', {"thank": thank, 'id': id})
        #paytm code
        data_dict = {
            'MID':'UkowTB87103086137667',
            'ORDER_ID':str(orders.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8001/shop/paymenthandler/',
        }
        data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'params':data_dict})
    return render(request, 'shop/checkout.html')


def termsandconditions(request):
    return HttpResponse("We are at checkout")


def privacy(request):
    return HttpResponse("We are at checkout")

@csrf_exempt
def paymenthandler(request):
    form = request.POST
    res_dict={}
    for i in form.keys():
        res_dict[i]=form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(res_dict,MERCHANT_KEY,checksum)
    if verify:
        if res_dict['RESPCODE'] == '01':
            print('order successfull')
        else:
            print('order unsuccessfull'+res_dict['RESPMSG'])
    return render(request,'shop/paymentstatus.html',{'response':res_dict})
