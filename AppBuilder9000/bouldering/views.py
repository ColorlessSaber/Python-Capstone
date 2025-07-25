from datetime import datetime, timedelta
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ClimbLogForm
from .models import User, ClimbLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def bouldering_home(request):
    last_ten_climbs = ClimbLog.climb_logs.all().order_by('-date')[0:10] # grab the last ten climb logs that were posted.
    context = {'past_logs': last_ten_climbs}
    return render(request, 'bouldering/bouldering-home-page.html', context)

def login_page(request):
    """
    handles the "login" page.

    :param request:
    :return:
    """
    form = UserForm(data=request.POST or None)
    if request.method == 'POST':
        # check to see if the account exists and the password is correct
        if form.is_valid():
            if User.users.filter(username=form.cleaned_data['username'], password=form.cleaned_data['password']).exists() :
                # pull user information and pass it along
                user_details = User.users.get(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                return redirect('user-climb-logs', user_pk=user_details.pk)
            else:
                # inform the user their username or password is incorrect
                content = {'form': form, 'message': 'Username or password is incorrect'}
                return render(request, 'bouldering/login-page.html', content)
        else:
            # if there is an error, take them back to the same screen
            content = {'form': form, 'message': 'Something went wrong. Please try again.'}
            return render(request, 'bouldering/login-page.html', content)
    else:
        content = {'form': form, 'message': ''}
        return render(request, 'bouldering/login-page.html', content)

def new_account(request):
    """
    Handles the "new account" page.

    :param request:
    :return:
    """
    form = UserForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # check to see if the account already exists
            if User.users.filter(username=request.POST['username']).exists():
                message = 'The username {} already exists!'.format(request.POST['username'])
                content = {'form': form, 'message': message}
                return render(request, 'bouldering/new-account.html', content)
            else:
                # save the new account and return the user to log-in screen
                new_user = form.save(commit=False)
                new_user.save()
                return redirect('login')
        else:
            # if there is an error, take them back to the same screen
            content = {'form': form, 'message': 'Something went wrong. Please try again.'}
            return render(request, 'bouldering/new-account.html', content)
    else:
        content = {'form': form, 'message': ''}
        return render(request, 'bouldering/new-account.html', content)

def load_user_climbs(request, user_pk):
    """
    Loads the user's climbs to a table while creating a paginator.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :return:
    """
    list_of_grades = [i[0] for i in ClimbLog.grade.field.choices] # get all available grades in the model for grade-filter
    user_details = get_object_or_404(User, pk=user_pk)
    page = request.GET.get('page', 1) # grab the page number currently displayed on screen

    if request.method == 'POST':
        # filter search based on grade filter selection
        # if "Clear Filter" was selected, return all data associated with the user who is logged in.
        print(request.POST.get('grade'))
        if request.POST.get('grade') != "Clear Filter":
            user_climbs = ClimbLog.climb_logs.filter(user=user_pk, grade=request.POST.get('grade')).order_by('-date')  # order records descending
        else:
            user_climbs = ClimbLog.climb_logs.filter(user=user_pk).order_by('-date')  # order records descending
    else:
        user_climbs = ClimbLog.climb_logs.filter(user=user_pk).order_by('-date')  # order records descending
    # create the paginator and logic
    paginator = Paginator(user_climbs, 5)
    try:
        user_climb_page = paginator.page(page)
    except PageNotAnInteger: # handles if the number cannot be converted to an integer
        user_climb_page = paginator.page(1)
    except EmptyPage: # raised if the first page is empty
        user_climb_page = paginator.page(paginator.num_pages)

    context = {
        'user': user_details,
        'climbs': user_climb_page,
        'list_of_grades': list_of_grades,
    }
    return render(request, 'bouldering/user-climb-logs.html', context)

def create_new_climb_log(request, user_pk):
    """
    Creates a new climb log for a user.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :return:
    """
    user_details = get_object_or_404(User, pk=user_pk)
    form = ClimbLogForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # save the climb log and return user to their overall climb log
            climb_log = form.save(commit=False)
            climb_log.user = user_details # assign the user to the climb log they wish to save
            climb_log.save()
            return redirect('user-climb-logs', user_pk=user_details.pk)
        else:
            # if there is an error, take them back to the same screen
            context = {'user': user_details, 'form': form, 'message': 'Something went wrong. Please try again.'}
            return render(request, 'bouldering/new-climb-log.html', context)
    else:
        context = {'user': user_details, 'form': form, 'message': ''}
        return render(request, 'bouldering/new-climb-log.html', context)

def load_climb_details(request, user_pk, climb_log_pk):
    """
    Loads the user's climb details in a line-by-line form.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :param climb_log_pk: The climb log primary key that identifies the climb log.
    :return:
    """
    user_details = get_object_or_404(User, pk=user_pk)
    climb_log = get_object_or_404(ClimbLog, pk=climb_log_pk)
    context = {
        'user': user_details,
        'climb_log': climb_log,
    }
    return render(request, 'bouldering/climb-log-details.html', context)

def edit_climb_log(request, user_pk, climb_log_pk):
    """
    Loads the appropriate page to allow the user to edit or delete the selected climb log.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :param climb_log_pk: The climb log primary key that identifies the climb log.
    :return:
    """
    user_details = get_object_or_404(User, pk=user_pk)
    climb_log = get_object_or_404(ClimbLog, pk=climb_log_pk)
    form = ClimbLogForm(data=request.POST or None, instance=climb_log)
    if request.method == 'POST':
        updated_climb_log = form.save(commit=False)
        updated_climb_log.save()
        return redirect('user-climb-logs', user_pk=user_pk)
    else:
        context = {'user': user_details, 'climb_log': climb_log, 'form': form}
        return render(request, 'bouldering/edit-climb-log.html', context)

def delete_climb_log(request, user_pk, climb_log_pk):
    """
    Deletes the selected climb log.

    This function is activated by a JS script in climb-log-details.html.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :param climb_log_pk: The climb log primary key that identifies the climb log.
    :return:
    """
    climb_log = get_object_or_404(ClimbLog, pk=climb_log_pk)

    # if the request is not a post, something happened during the request to delete the climb log.
    # inform the user of this by setting 'success' to false.
    if request.method != 'POST':
        return JsonResponse({'success': False})

    # delete the climb log and have the JavaScript that called this function return user back to the
    # user's climb logs page
    climb_log.delete()
    return JsonResponse(
        {
            'success': True,
            'redirect_url': reverse(
                'user-climb-logs', kwargs={'user_pk': user_pk}
            )
        }
    )