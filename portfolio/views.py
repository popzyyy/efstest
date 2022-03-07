from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .models import *
from .forms import *
import csv
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
now = timezone.now()
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout as bruh
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from fpdf import FPDF
from django.core.mail import EmailMessage
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)


@login_required
def pdf(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutuals = Mutual.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))

    total_initial_investment = 0
    total_current_investment = 0
    sum_of_initial_stock_value = 0
    sum_of_current_stock_value = 0

    sum_of_initial_mutual_value = 0
    sum_of_current_mutual_value = 0

    for investment in investments:
        total_initial_investment += investment.acquired_value
        total_current_investment += investment.recent_value

    for stock in stocks:
        sum_of_initial_stock_value += stock.initial_stock_value()
        sum_of_current_stock_value += stock.current_stock_value()
    for mutual in mutuals:
        sum_of_initial_mutual_value += mutual.initial_mutual_value()
        sum_of_current_mutual_value += mutual.current_mutual_value()

    investment_result = total_current_investment - total_initial_investment
    stock_result = sum_of_current_stock_value - sum_of_initial_stock_value
    mutual_result = sum_of_current_mutual_value - sum_of_initial_mutual_value

    str_investment_result = str(investment_result)
    str_stock_result = str(stock_result)
    str_mutual_result = str(mutual_result)

    str_sum_of_initial_stock_value = str(sum_of_initial_stock_value)
    str_sum_of_current_stock_value = str(sum_of_current_stock_value)
    str_total_initial_investment = str(total_initial_investment)
    str_total_current_investment = str(total_current_investment)
    str_sum_of_initial_mutual_value = str(sum_of_initial_mutual_value)
    str_sum_of_current_mutual_value = str(sum_of_current_mutual_value)

    total_portfolio = sum_of_current_stock_value + sum_of_current_mutual_value + total_current_investment
    total_portfolio = str(total_portfolio)
    url = 'http://api.currencylayer.com/live?access_key='
    api_key = '31ee563c7d5295a62ed091f48b11955c'
    currency_format = '&format=1'
    USD = '&source=USD'
    CAD = '&currencies=CAD'
    convert_url = url + api_key + USD + CAD + currency_format
    currency_conversion = requests.get(convert_url).json()

    CAD = currency_conversion["quotes"]["USDCAD"]
    str_CAD = str(CAD)
    convert = float(CAD) * float(total_portfolio)
    str_convert = str(convert)
    data = [
        {"item": "Stocks", "amount": '$'+str_stock_result},
        {"item": "Investments", "amount": '$'+str_investment_result},
        {"item": "Mutual Funds", "amount": '$'+str_mutual_result},

    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Customer Portfolio', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Category of Gain'.ljust(30)} {'Gain in Dollars'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.cell(40, 10, '', 0, 1)

    category_data = [{"item": 'Stocks:  $'+str_sum_of_initial_stock_value, "amount": '$'+str_sum_of_current_stock_value},
                     {"item": 'Investments:  $' + str_total_initial_investment, "amount": '$' + str_total_current_investment},
                     {"item": 'Mutual Funds:  $' + str_sum_of_initial_mutual_value, "amount": '$' + str_sum_of_current_mutual_value},
                     ]

    pdf.cell(200, 8, f"{'Initial Value'.ljust(30)} {'Current Value'.rjust(20)}", 0, 1)
    pdf.line(10, 72, 150, 72)
    pdf.line(10, 80, 150, 80)
    for line in category_data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.line(10, 115, 150, 115)
    pdf.line(10, 123, 150, 123)
    pdf.cell(200, 8, f"{'Total Portfolio Value USD'.ljust(30)} {'Total Portfolio Value CAD'.rjust(20)}", 0, 1)
    total_data = [{"item": '$'+total_portfolio, "amount":'$'+str_convert}]
    for line in total_data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.output('portfolio.pdf', 'F')
    return FileResponse(open('portfolio.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

@login_required
def email_pdf(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutuals = Mutual.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))

    total_initial_investment = 0
    total_current_investment = 0
    sum_of_initial_stock_value = 0
    sum_of_current_stock_value = 0

    sum_of_initial_mutual_value = 0
    sum_of_current_mutual_value = 0

    for investment in investments:
        total_initial_investment += investment.acquired_value
        total_current_investment += investment.recent_value

    for stock in stocks:
        sum_of_initial_stock_value += stock.initial_stock_value()
        sum_of_current_stock_value += stock.current_stock_value()
    for mutual in mutuals:
        sum_of_initial_mutual_value += mutual.initial_mutual_value()
        sum_of_current_mutual_value += mutual.current_mutual_value()

    investment_result = total_current_investment - total_initial_investment
    stock_result = sum_of_current_stock_value - sum_of_initial_stock_value
    mutual_result = sum_of_current_mutual_value - sum_of_initial_mutual_value

    str_investment_result = str(investment_result)
    str_stock_result = str(stock_result)
    str_mutual_result = str(mutual_result)

    str_sum_of_initial_stock_value = str(sum_of_initial_stock_value)
    str_sum_of_current_stock_value = str(sum_of_current_stock_value)
    str_total_initial_investment = str(total_initial_investment)
    str_total_current_investment = str(total_current_investment)
    str_sum_of_initial_mutual_value = str(sum_of_initial_mutual_value)
    str_sum_of_current_mutual_value = str(sum_of_current_mutual_value)

    total_portfolio = sum_of_current_stock_value + sum_of_current_mutual_value + total_current_investment
    total_portfolio = str(total_portfolio)
    url = 'http://api.currencylayer.com/live?access_key='
    api_key = '31ee563c7d5295a62ed091f48b11955c'
    currency_format = '&format=1'
    USD = '&source=USD'
    CAD = '&currencies=CAD'
    convert_url = url + api_key + USD + CAD + currency_format
    currency_conversion = requests.get(convert_url).json()

    CAD = currency_conversion["quotes"]["USDCAD"]
    str_CAD = str(CAD)
    convert = float(CAD) * float(total_portfolio)
    str_convert = str(convert)
    data = [
        {"item": "Stocks", "amount": '$'+str_stock_result},
        {"item": "Investments", "amount": '$'+str_investment_result},
        {"item": "Mutual Funds", "amount": '$'+str_mutual_result},

    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Customer Portfolio', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Category of Gain'.ljust(30)} {'Gain in Dollars'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.cell(40, 10, '', 0, 1)

    category_data = [{"item": 'Stocks:  $'+str_sum_of_initial_stock_value, "amount": '$'+str_sum_of_current_stock_value},
                     {"item": 'Investments:  $' + str_total_initial_investment, "amount": '$' + str_total_current_investment},
                     {"item": 'Mutual Funds:  $' + str_sum_of_initial_mutual_value, "amount": '$' + str_sum_of_current_mutual_value},
                     ]

    pdf.cell(200, 8, f"{'Initial Value'.ljust(30)} {'Current Value'.rjust(20)}", 0, 1)
    pdf.line(10, 72, 150, 72)
    pdf.line(10, 80, 150, 80)
    for line in category_data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.line(10, 115, 150, 115)
    pdf.line(10, 123, 150, 123)
    pdf.cell(200, 8, f"{'Total Portfolio Value USD'.ljust(30)} {'Total Portfolio Value CAD'.rjust(20)}", 0, 1)
    total_data = [{"item": '$'+total_portfolio, "amount":'$'+str_convert}]
    for line in total_data:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.output('portfolio.pdf', 'F')

    user = request.user
    email_msg = EmailMessage(
        'Portfolio Report',
        'Attached is your Portfolio Report PDF',
        'popzyyy0@gmail.com',
        [user.email],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
    )
    email_msg.attach_file('portfolio.pdf')
    email_msg.send()
    context = {}
    return render(request, 'portfolio/portfolio.html', context=context)

@login_required
def export_csv(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutuals = Mutual.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))

    total_initial_investment = 0
    total_current_investment = 0
    sum_of_initial_stock_value = 0
    sum_of_current_stock_value = 0

    sum_of_initial_mutual_value = 0
    sum_of_current_mutual_value = 0

    for investment in investments:
        total_initial_investment += investment.acquired_value
        total_current_investment += investment.recent_value

    for stock in stocks:
        sum_of_initial_stock_value += stock.initial_stock_value()
        sum_of_current_stock_value += stock.current_stock_value()
    for mutual in mutuals:
        sum_of_initial_mutual_value += mutual.initial_mutual_value()
        sum_of_current_mutual_value += mutual.current_mutual_value()

    investment_result = total_current_investment - total_initial_investment
    stock_result = sum_of_current_stock_value - sum_of_initial_stock_value
    mutual_result = sum_of_current_mutual_value - sum_of_initial_mutual_value

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="portfolio.csv"'

    writer = csv.writer(response)
    stocks = Stock.objects.all()
    mutuals = Mutual.objects.all()
    investments = Investment.objects.all()

    with open("Expired_Kits_In_Studies_Report.csv", "w"):
            writer.writerow(stocks.objects.values('symbol'))
            writer.writerow(stocks.objects.values('name'))
            writer.writerow(stocks.objects.values('shares'))
            writer.writerow(stocks.objects.values('purchase_price'))

    return FileResponse(open('portfolio.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


@login_required
def portfolio(request, pk):
              #stock_name):

    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutuals = Mutual.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=F4NTI9HSI62830VF'
    r = requests.get(url)
    data = r.json()

    url = 'http://api.currencylayer.com/live?access_key='
    api_key = '31ee563c7d5295a62ed091f48b11955c'
    currency_format = '&format=1'
    USD = '&source=USD'
    CAD = '&currencies=CAD'
    convert_url = url + api_key + USD + CAD + currency_format
    currency_conversion = requests.get(convert_url).json()

    CAD = currency_conversion["quotes"]["USDCAD"]

    total_initial_investment = 0
    total_current_investment = 0
    sum_of_initial_stock_value = 0
    sum_of_current_stock_value = 0

    sum_of_initial_mutual_value = 0
    sum_of_current_mutual_value = 0

    for investment in investments:
        total_initial_investment += investment.acquired_value
        total_current_investment += investment.recent_value

    for stock in stocks:
        #sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()
        sum_of_current_stock_value += stock.current_stock_value()
    for mutual in mutuals:
        sum_of_initial_mutual_value += mutual.initial_mutual_value()
        sum_of_current_mutual_value += mutual.current_mutual_value()

    investment_result = total_current_investment - total_initial_investment
    stock_result =  sum_of_current_stock_value - sum_of_initial_stock_value
    mutual_result = sum_of_current_mutual_value - sum_of_initial_mutual_value

    total_portfolio = sum_of_current_stock_value + sum_of_current_mutual_value + total_current_investment
    print(investment_result)
    print(stock_result)
    print(mutual_result)

    str_investment_result = str(investment_result)
    str_stock_result = str(stock_result)
    str_mutual_result = str(mutual_result)


    data = [str_investment_result, str_stock_result, str_mutual_result]
    labels = ['Investments', 'Stocks', 'Mutual Funds']





    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'mutuals': mutuals,
                                                        'total_initial_investment': total_initial_investment,
                                                        'total_current_investment': total_current_investment,
                                                        'investment_result': investment_result,
                                                        'sum_of_current_stock_value': sum_of_current_stock_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                        'stock_result':stock_result,
                                                        'mutual_result':mutual_result,
                                                        'sum_of_current_mutual_value':sum_of_current_mutual_value,
                                                        'sum_of_initial_mutual_value':sum_of_initial_mutual_value,
                                                        'CAD':CAD,
                                                        'data':data,
                                                        'labels':labels,

                                                        })

def home(request):
    return render(request, 'portfolio/home.html',
                  {'portfolio': home})

@login_required
def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_date = timezone.now()
            customer.save()
            customers = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customers})
    else:
        form = CustomerForm()
        # print("Else")
    return render(request, 'portfolio/customer_new.html', {'form': form})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                  {'customers': customer})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


def stock_new(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html',
                          {'stocks': stocks})
    else:
        form = StockForm()
        # print("Else")
    return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            # stock.customer = stock.id
            stock.updated_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
    else:
        # print("else")
        form = StockForm(instance=stock)
    return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def investment_list(request):
    investments = Investment.objects.filter(recent_date__lte=timezone.now())
    #total_investment = Investment.objects.values(instance="recent_value")
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            # stock.customer = stock.id
            investment.updated_date = timezone.now()
            investment.save()
            investment = Investment.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investment': investment})
    else:
        # print("else")
        form = InvestmentForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')


@login_required
def investment_new(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.created_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html',
                          {'investments': investments})
    else:
        form = InvestmentForm()
        # print("Else")
    return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return redirect('portfolio:stock_list')


@login_required
def fund_delete(request, pk):
    funds = get_object_or_404(Fund, pk=pk)
    funds.delete()
    return redirect('portfolio:fund_list')


@login_required
def fund_edit(request, pk):
    investment = get_object_or_404(Fund, pk=pk)
    if request.method == "POST":
        form = FundForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            # stock.customer = stock.id
            investment.updated_date = timezone.now()
            investment.save()
            investment = Fund.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/fund_list.html', {'investment': investment})
    else:
        # print("else")
        form = FundForm(instance=investment)
    return render(request, 'portfolio/fund_edit.html', {'form': form})


@login_required
def fund_list(request):
    funds = Fund.objects.all()
    return render(request, 'portfolio/fund_list.html', {'funds': funds})


@login_required
def fund_new(request):
    if request.method == "POST":
        form = FundForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            fund.created_date = timezone.now()
            fund.save()
            funds = Fund.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/fund_list.html',
                          {'funds': funds})
    else:
        form = FundForm()
        # print("Else")
    return render(request, 'portfolio/fund_new.html', {'form': form})



@login_required
def mutual_new(request):
    if request.method == "POST":
        form = MutualForm(request.POST)
        if form.is_valid():
            mutual = form.save(commit=False)
            mutual.created_date = timezone.now()
            mutual.save()
            mutuals = Mutual.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/mutual_list.html',
                          {'mutuals': mutuals})
    else:
        form = MutualForm()
        # print("Else")
    return render(request, 'portfolio/mutual_new.html', {'form': form})

@login_required
def mutual_list(request):
    mutuals = Mutual.objects.all()
    return render(request, 'portfolio/mutual_list.html', {'mutuals': mutuals})

@login_required
def mutual_edit(request, pk):
    mutual = get_object_or_404(Mutual, pk=pk)
    if request.method == "POST":
        form = MutualForm(request.POST, instance=mutual)
        if form.is_valid():
            mutual = form.save()
            mutual.updated_date = timezone.now()
            mutual.save()
            mutual = Mutual.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/fund_list.html', {'mutual': mutual})
    else:
        # print("else")
        form = MutualForm(instance=mutual)
    return render(request, 'portfolio/fund_edit.html', {'form': form})

@login_required
def mutual_delete(request, pk):
    mutual = get_object_or_404(Mutual, pk=pk)
    mutual.delete()
    return redirect('portfolio:mutual_list')

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'