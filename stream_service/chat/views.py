from django.core import serializers
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from .forms import UserForm
from .models import Message


@login_required
def home(request):
    chat_queryset = Message.objects.order_by("-created")[:10]
    chat_message_count = len(chat_queryset)

    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset) - 1].id
    else:
        first_message_id = -1

    previous_id = -1

    if first_message_id != -1:
        try:
            previous_id = Message.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
        except IndexError:
            previous_id = -1

    chat_messages = reversed(chat_queryset)

    return render(request, "home.html", {
        'chat_messages': chat_messages,
        'first_message_id': previous_id,
    })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)

    return render(request, 'profile.html', {
        'user_form': user_form
    })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def get_all_messages(request, user_alias):

    messages = Message.objects.filter(user__alias=user_alias).order_by('-created').values('message', 'created')[:20]

    return JsonResponse({'results': list(messages)})

