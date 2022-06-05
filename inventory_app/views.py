from django.contrib import messages
from django.shortcuts import render, redirect
import csv
# from .models import User
from .models import *
from .form import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_user

from django.core.mail import send_mail

# get questions and display them
from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html')


# def modRegisterPage(request):
#     form = UserCreationForm
#
#
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#     context = {'form': form}
#
#     return render(request, 'modRegister.html', context)

@unauthenticated_user
def modLoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mod')

    context = {}
    return render(request, 'modLogin.html', context)


def logoutMod(request):
    logout(request)
    return redirect('login')


@login_required
@allowed_user(allowed_roles=['moderator'])
def mod(request):
    return render(request, "mod.html")


def add_items(request):
    adder = Customer.objects.get_or_create(customer=request.user)
    (c, torf) = adder
    obj = Item.objects.create(madeby =c )
    form = StockCreateForm(request.POST or None , instance = obj)

    if form.is_valid():
        instance = form.save(commit=False)
        obj. created_number = instance.quantity
        instance.save()
        obj.save()

        items = Item.objects.all()
        for it in items:
            if it.item_name is None:
                it.delete()

        return redirect('/mod')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_item.html", context)


@login_required
@allowed_user(allowed_roles=['moderator'])
def update_items(request, pk):
    queryset = Item.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/update_items/')

    context = {
        'form': form
    }
    return render(request, 'add_item.html', context)


@login_required
@allowed_user(allowed_roles=['moderator'])
def update_items_list(request):
    form = StockSearchForm(request.POST or None)

    queryset = Item.objects.all()
    context = {'queryset': queryset, }
    context = {
        "form": form,
        "queryset": queryset,
    }

    if request.method == 'POST':
        queryset = Item.objects.filter(category__icontains=form['category'].value(),
                                       item_name__icontains=form['item_name'].value()
                                       )
        context = {
            "form": form,
            "queryset": queryset,
        }

    return render(request, 'update_itemlist.html', context)


@login_required
@allowed_user(allowed_roles=['moderator'])
def delete_items(request, pk):
    queryset = Item.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/update_items/')
    return render(request, 'delete_items.html')


@login_required
@allowed_user(allowed_roles=['moderator'])
def upload_file_view(request):
    form = CsvModelForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated = False)
        with open(obj .file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i,row in  enumerate(reader):
                if i ==0:
                    pass
                else:
                    product_name = row[0]
                    adder = Customer.objects.get_or_create(customer=request.user)
                    (c, torf) = adder
                    user = c
                    cat = row[1]
                    number = int(row[2])
                    Item.objects.create(
                        item_name = product_name,
                        quantity = number,
                        category = cat,
                        madeby = c,
                        created_number = number

                    )


            obj.activated= True
            obj.save()
            return redirect('/mod/')
    return render(request , "upload.html" , {'form': form})


@login_required
def list_items(request):
    form = StockSearchForm(request.POST or None)

    issue = Issue.objects.all()
    for obj in issue:
        if obj.numberofitems == 0:
            obj.delete()
    queryset = Item.objects.all()
    context = {'queryset': queryset, }
    context = {
        "form": form,
        "queryset": queryset,
    }

    if request.method == 'POST':
        queryset = Item.objects.filter(category__icontains=form['category'].value(),
                                       item_name__icontains=form['item_name'].value()
                                       )
        context = {
            "form": form,
            "queryset": queryset,
        }

    return render(request, 'list_item.html', context)


def issue_items(request, pk):
    cust = Customer.objects.get_or_create(customer=request.user)
    (c, torf) = cust
    obj = Item.objects.get(id=pk)
    issuing = Issue.objects.create(customer=c, item=obj)

    form = IssueForm(request.POST or None, instance=issuing)

    if form.is_valid():
        instance = form.save(commit=False)
        obj.quantity = obj.quantity - instance.numberofitems
        instance.save()
        obj.save()

        send_mail(
            'Item Issued Successfully!',
            str(instance.numberofitems) + " " + obj.item_name + " issued from your account",
            'djangotest1901@gmail.com',
            ['sanju.saurav0@gmail.com'],
            fail_silently=False

        )

        return redirect('/list_item/')

    context = {
        "title": 'Issue ' + str(obj.item_name),
        "queryset": obj,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_item.html", context)


def item_detail(request, pk):
    queryset = Item.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


def return_item(request, pk):
    if request.method == 'POST':
        returnobj = Issue.objects.get(id=pk)
        returnitem = returnobj.item
        returnobj.returned = True
        returnitem.quantity += returnobj.numberofitems
        returnitem.save()
        returnobj.save()

        return redirect('/accounts/profile')
    return render(request, 'return_item.html')


def profilepage(request):
    cust = Customer.objects.get_or_create(customer=request.user)
    (c, torf) = cust
    items_to_return = Issue.objects.filter(customer=c)
    context = {"items_to_return": items_to_return}
    return render(request, "profile.html", context)


def exportIssue(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Number Issued', 'Returned', 'Issued by'])
    for obj in Issue.objects.all():
        itname = obj.item.item_name
        usern = obj.customer.customer.username

        writer.writerow([itname, obj.numberofitems, obj.returned, usern])
    response['Content-Disposition'] = 'attachement; filename="issue_data.csv"'
    return response


def exportCreation(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Item Name','Category', 'Number Made' ,'Made by'])
    for obj in Item.objects.all():
        usern = obj.madeby.customer.username

        writer.writerow([obj.item_name,obj.category, obj.created_number, usern])
    response['Content-Disposition'] = 'attachement; filename="Item_creation_data.csv"'
    return response



