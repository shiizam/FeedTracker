from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic

from django.db import IntegrityError

from .models import User, FormulaLog, Weight
from .forms import EditProfileForm, ChangePasswordForm

from collections import Counter
import datetime 

# User Profile Settings
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('feeds:edit_profile')
    
    def get_object(self):
        return self.request.user  

# Home page
def index(request):
    return render(request,'index.html')


""" Views for User Registraion, login/logout """ 

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        feed_goal = 0 # sets default feed goal to 0 

        password = request.POST['password']
        confirm_password = request.POST['confirmation']

        if password != confirm_password:
            return render(request, 'register.html', {
                'message': 'Passwords do not match! Please try again',
            })

        try:
            user = User.objects.create_user(username,email,first_name=first_name,last_name=last_name,feed_goal=feed_goal)
            user.save()
        except IntegrityError:
            return render(request,'register.html', {
                'message':'Username exists',
            })

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request,'register.html')
    

@login_required
def change_password(request):
    if request.method == 'POST':

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['new_password2']
            username = request.user.username
            password = form.cleaned_data['old_password']

            user = authenticate(username=username, password=password)

            if user is not None:
                user.set_password(newpassword)
                user.save()
                return HttpResponseRedirect(reverse_lazy('feeds:password_success'))
            else:
                return render(request,'change-password.html')
        else:
                return render(request,'change-password.html')
    else:
        form = ChangePasswordForm()  
        return render(request, 'change-password.html', {'form': form})


# Password Changed Success Page
def password_success(request):
    return render(request, 'password-changed.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('feeds:feedlog'))
        else:
            return render(request, 'login.html', {
                'message':'username or password is invalid. Please try again.'
            })
    
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html')


""" Feed Dashboard functions """

@login_required
def feed_log_view(request):
    previous_entries = FormulaLog.objects.all()
    filter_date = []
    filter_entries = []
    user = request.user

    if request.method == 'POST':
        if 'logentry' in request.POST:

            time_of_feed = request.POST.get('time')
            feed_amount = request.POST.get('amount')
            
            if time_of_feed and feed_amount != '':

                # Converts user data to metric so that all data is in metric once saved in Database
                if user.units == 'IMPERIAL':
                    feed_amount = round(float(feed_amount) * 29.574) 
                else:
                    feed_amount = feed_amount

                feed_log = FormulaLog(user=user,time_of_feed=time_of_feed,feed_amount=feed_amount)
                feed_log.save()
                return HttpResponseRedirect(reverse('feeds:feedlog'))
            
        # Filter to allow User to pick previous date and see entries on said date
        elif 'logfilter' in request.POST:
            get_filter_date = request.POST.get('dayfilter')
            filter_date = datetime.datetime.strptime(get_filter_date, '%Y-%m-%d').date()

            if filter_date != datetime.datetime.today():
                filter_entries = FormulaLog.objects.filter(date_created=filter_date)

        else:
            return HttpResponse('Empty or invalid field(s). Please check that you have all field(s) completed')

    user_feed_log = FormulaLog.objects.filter(user=user)
    
    return render(request,'user_dashboard.html', {
        'previous_entries':previous_entries,
        'user_feed_log':user_feed_log,
        'filter_date': filter_date,
        'filter_entries': filter_entries,
    })


@login_required
def feed_log_delete(request,formulalog_id):
    previous_entries = FormulaLog.objects.filter(id=formulalog_id)

    if request.method == 'POST':
        previous_entries.delete()
        return HttpResponseRedirect(reverse('feeds:feedlog'))
    
    return render(request, 'feed_log_delete.html')


""" 
Chart Data Views
- These views are used for the charts that are found on the feed log dashboard for each user.
"""

@login_required
def daily_data(request):

    today = datetime.date.today()
    user_feeds = FormulaLog.objects.filter(user=request.user,date_created__day=today.day).values_list('date_created','feed_amount')

    # Loop through user_feeds variable and get dates and total sum of feeds for each day 
    feed_count_date = Counter([feed[0] for feed in user_feeds])
    feed_amount_date = {}

    for date in feed_count_date:
        feed_amount_date[date] = 0

    for feed in user_feeds:
        for date in feed_amount_date:
            if feed[0] == date:
                feed_amount_date[date] += feed[1]

    units = request.user.units

    data_dict = {
        "labels":list(feed_count_date.keys()),
        "data":list(feed_amount_date.values()),
        'units':units
    }
    
    return JsonResponse(data=data_dict,safe=False)

@login_required
def weekly_data(request):
    
    today = datetime.date.today()
    d=today-datetime.timedelta(days=7)
    daily_feeds = FormulaLog.objects.filter(user=request.user, date_created__gte=d).values_list('date_created','feed_amount').order_by('-date_created')

    weekly_feeds_date = Counter([feed[0] for feed in daily_feeds])
    weekly_total_amount = {}

    # Loop through user_feeds variable and get dates and total sum of feeds for each day 
    for date in weekly_feeds_date:
        weekly_total_amount[date] = 0

    for feed in daily_feeds:
        for date in weekly_total_amount:
            if feed[0] == date:
                weekly_total_amount[date] += feed[1]

    units = request.user.units
    metric_data = list(weekly_total_amount.values())

    # Converts (if user is using imperial) data before sending JSON to chart functions
    if units == 'IMPERIAL':
        data = [round(value/29.574) for value in metric_data]
    

    else:
        data = list(weekly_total_amount.values())

    data_dict = {
        "labels":list(weekly_feeds_date.keys()),
        "data":data,
    }

    return JsonResponse(data=data_dict,safe=False)

@login_required
def monthly_data(request):
    
    today = datetime.date.today()
    user_feeds = FormulaLog.objects.filter(user=request.user,date_created__month=today.month).values_list('date_created','feed_amount').order_by('-date_created')
    
    # Loop through user_feeds variable and get dates and total sum of feeds for each day 
    feed_count_date = Counter([feed[0] for feed in user_feeds])
    feed_amount_date = {}

    for date in feed_count_date:
        feed_amount_date[date] = 0

    for feed in user_feeds:
        for date in feed_amount_date:
            if feed[0] == date:
                feed_amount_date[date] += feed[1]

    metric_data = list(feed_amount_date.values())
    units = request.user.units

    # Converts (if user is using imperial) data before sending JSON to chart functions
    if units == 'IMPERIAL':
        data = [round(value/29.574) for value in metric_data]

    else:
        data = list(feed_amount_date.values())

    data_dict = {
        "labels":list(feed_count_date.keys()),
        "data":data,
    }

    return JsonResponse(data=data_dict,safe=False)


"""
Weight Log Views

WEIGHT_LOG VIEW
- Allows user to enter weights and creates a log and graph for user entries
- Converts all data to metric regardless of user preference before saving to Database.
  Then is converted again on load depending on User preferences via custom filter tags.

WEIGHT_LOG_DELETE VIEW
- Allows User the abilty to delete entries from Database
"""

@login_required
def weight_log(request):

    previous_weights = Weight.objects.all()

    if request.method == 'POST':

        weight = request.POST.get('weight')
        date = request.POST.get('date')
        
        if date and weight != '':
            user = request.user

            if user.units == 'IMPERIAL':
                lbs = request.POST.get('lbs')
                oz = request.POST.get('oz')
                weight = round((int(lbs) / 2.205)+(int(oz) / 35.274),3)

            else:
                weight = weight

            weight_log = Weight(user=user,weight=weight,date=date)
            weight_log.save()

            return HttpResponseRedirect(reverse('feeds:weightlog'))

        else:
            return HttpResponse('Empty or invalid field(s). Please check that you have all field(s) completed')
    
    # Used to make log only keep monthly data before starting over fresh
    month = datetime.date.today()
    user_weight_log = Weight.objects.filter(user=request.user,date__month=month.month)
    
    return render(request, 'weight_dashboard.html',{
        'previous_weights': previous_weights,
        'user_weight_log': user_weight_log,
    })


@login_required
def weight_log_delete(request,weight_id):
    previous_entries = Weight.objects.filter(id=weight_id)

    if request.method == 'POST':
        previous_entries.delete()
        return HttpResponseRedirect(reverse('feeds:weightlog'))
    
    return render(request, 'weight_log_delete.html')
