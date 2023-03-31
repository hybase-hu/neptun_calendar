import datetime
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from my_calendar.models import NeptunUser, NeptunClass


def login_view(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST and len(request.POST['username']) > 3 and \
                len(request.POST['password']) > 4:
            username = request.POST['username'].lower()
            password = request.POST['password']
            try:
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.warning(request, "Nincs ilyen felhasználó vagy téves jelszó")
                else:
                    login(request, user)
                    return redirect("/")
            except Exception as e:

                messages.warning(request, e)
        else:
            messages.warning(request, "Nem kitöltött adatok")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST and len(request.POST['username']) > 3 and \
                len(request.POST['password']) > 4:

                if request.POST['password'] != request.POST['password2']:
                    messages.warning(request, "Nem egyezik a jelszó")
                else:
                    username = request.POST['username'].lower()
                    password = request.POST['password']
                    try:
                        user = User.objects.create_user(username=username, password=password)
                        neptun_user = NeptunUser.objects.create(user=user)
                        neptun_user.save()

                        login(request, user)
                        return redirect("/")
                    except Exception as e:
                        messages.warning(request, e)


        else:
            if len(request.POST['password']) < 4:
                messages.warning(request, "A jelszó legyen legalább 5 karakter, nah")
            messages.warning(request, "Nem kitöltött adatok")

    return render(request, "register.html")


def logout_view(request):
    logout(request=request)
    return redirect("/login")


@login_required(login_url="/login", redirect_field_name="/")
def calendar_view(request):
    context = list()
    user = request.user
    neptun_user = NeptunUser.objects.get(user=user)

    if '.csv' not in neptun_user.calendar.name:
        messages.warning(request, "Nincs feltöltve .csv formátumú órarended!")
        return redirect("/update")

    try:
        with open((os.path.join(settings.MEDIA_ROOT, neptun_user.calendar.name)), 'r', encoding='ISO-8859-2') as csv:
            content = csv.readlines()

            for row in content:
                csv_data = row.split(';')
                try:
                    c = NeptunClass(start=csv_data[0], end=csv_data[1], desc=csv_data[2], local=csv_data[3])
                    context.append(c)
                except Exception as e:
                    messages.warning(request, "Hiba történt egy adat feldolgozásában", e)

    except Exception as e:
        print(e)
        messages.warning(request, "Hiba történt " + e)

    # rendezés
    dated_list = [context for context in context if
                  context.start > (datetime.datetime.now() - datetime.timedelta(days=1))]
    context = sorted(dated_list, key=lambda x: x.start)

    return render(request, "my_calendar/calendar.html", context={"data": context, "neptun_user": neptun_user})


@login_required(login_url="/login", redirect_field_name="/")
def calendar_update(request):
    if request.method == 'POST':

        if 'data' in request.FILES:
            user = request.user
            neptun_user = NeptunUser.objects.get(user=user)
            if neptun_user is not None:
                neptun_user.calendar = request.FILES['data']
                neptun_user.uploaded_calendar = datetime.datetime.now()
                neptun_user.save()
                return redirect("/")
            else:
                messages.warning(request, "Nem sikerült")
        else:
            print("not post")

    return render(request, "my_calendar/update_calendar.html")
