import csv
import datetime
import json

import openpyxl
from openpyxl import Workbook

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from ecommerce.models import Customer
from ecommerce.forms import CustomerModelForm
from django.core.paginator import Paginator


# Create your views here.


def project_management(request):
    return render(request, 'ecommerce/project-management.html')


# def customers(request):
#     search_query = request.GET.get('search', '')
#     customers = Customer.objects.all()
#     paginator = Paginator(customers, 3)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     if search_query:
#         customers = customers.filter(
#             Q(first_name__icontains=search_query) |
#             Q(last_name__icontains=search_query) |
#             Q(email__icontains=search_query)
#         )
#
#     context = {
#         'customers': page_obj
#     }
#     return render(request, 'ecommerce/customers.html', context)

class CustomerModelFormView(View):
    def get(self, request):
        search_query = request.GET.get('search')
        customers = Customer.objects.all()
        paginator = Paginator(customers, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if search_query:
            customers = customers.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        context = {
            'customers': page_obj
        }
        return render(request, 'ecommerce/customers.html', context)


# def customer_details(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     context = {'customer': customer}
#     return render(request, 'ecommerce/customer-details.html', context)


class CustomerDetailsView(View):
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer = get_object_or_404(Customer, id=customer_id)
        customer = Customer.objects.get(id=customer.id)
        context = {'customer': customer}
        return render(request, 'ecommerce/customer-details.html', context)


def profile(request):
    return render(request, 'ecommerce/profile.html')


def profile_settings(request):
    return render(request, 'ecommerce/settings.html')


# def add_customer(request):
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     else:
#         form = CustomerModelForm()
#
#     context = {'form': form}
#     return render(request, 'ecommerce/add-customer.html', context)


class CustomerCreateView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'ecommerce/add-customer.html', {"form": form})

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def edit_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     form = CustomerModelForm(instance=customer)
#
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('ecommerce')
#     else:
#         form = CustomerModelForm(instance=customer)
#
#     context = {'form': form}
#     return render(request, 'ecommerce/edit-customer.html', context)


class CustomerUpdateView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(instance=customer)
        return render(request, 'ecommerce/settings.html', {'form': form, 'customer': customer})

    def post(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect("customer_details", customer_id)


# def delete_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#
#     if request.method == "POST":
#         customer.delete()
#         return redirect('ecommerce')
#
#     return render(request, 'ecommerce/delete-customer.html', {'customer': customer})

class CustomerDeleteView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)

        if request.method == "POST":
            customer.delete()
            return redirect('ecommerce')

        return render(request, 'ecommerce/delete-customer.html', {'customer': customer})


from django.http import HttpResponse, JsonResponse
from django.views import View
from openpyxl import Workbook
import csv
import json
import datetime

class ExportDataView(View):
    model = Customer
    field_names = None

    def get(self, request, *args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        export_format = request.GET.get('format')

        if not self.field_names:
            meta = self.model._meta
            self.field_names = [field.name for field in meta.fields]

        if export_format == 'csv':
            return self.export_as_csv(date)
        elif export_format == 'json':
            return self.export_as_json(date)
        elif export_format == 'xlsx':
            return self.export_as_excel(date)
        else:
            return HttpResponse(status=400, content='Invalid format')

    def export_as_csv(self, date):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.object_name}-{date}.csv'
        writer = csv.writer(response)
        writer.writerow(self.field_names)
        for obj in self.model.objects.all():
            writer.writerow([getattr(obj, field) for field in self.field_names])
        return response

    def export_as_json(self, date):
        data = list(self.model.objects.all().values('id', 'full_name', 'phone', 'email'))
        response = JsonResponse(data, safe=False, json_dumps_params={'indent': 4})
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.object_name}-{date}.json'
        return response

    def export_as_excel(self, date):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Customers"
        worksheet.append(self.field_names)
        for obj in self.model.objects.all():
            row = [getattr(obj, field) for field in self.field_names]
            worksheet.append(row)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.object_name}-{date}.xlsx'
        workbook.save(response)
        return response

