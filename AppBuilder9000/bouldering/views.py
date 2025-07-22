from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ClimbLogForm
from .models import User, ClimbLog
# Create your views here.
def bouldering_home(request):
    return render(request, 'bouldering/bouldering-home-page.html')

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
    Loads the user's climbs to a table.

    :param request:
    :param user_pk: The primary key that identifies the user in the database who logged in.
    :return:
    """
    user_details = get_object_or_404(User, pk=user_pk)
    user_climbs = ClimbLog.climb_logs.filter(user=user_details).order_by('-date') # order records descending
    context = {'user': user_details, 'climbs': user_climbs}
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