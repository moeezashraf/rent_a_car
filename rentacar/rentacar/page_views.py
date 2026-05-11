from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def car_list(request):
    return render(request, 'cars/car_list.html')

def car_detail(request, pk):
    return render(request, 'cars/car_detail.html', {'car_id': pk})

# Auth pages
def login_page(request):
    return render(request, 'accounts/login.html')

def register_page(request):
    return render(request, 'accounts/register.html')

# Dashboard pages
def customer_dashboard(request):
    return render(request, 'dashboards/customer_dashboard.html')

def owner_dashboard(request):
    return render(request, 'dashboards/owner_dashboard.html')

def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')