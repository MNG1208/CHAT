# messaging/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import SignUpForm, MessageForm
from .models import Message
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inbox')
    else:
        form = SignUpForm()
    return render(request, 'messaging/signup.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        recipient_username = request.POST.get('recipient')
        try:
            recipient = User.objects.get(username=recipient_username)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.recipient = recipient
                message.save()
                return redirect('inbox')
        except User.DoesNotExist:
            form.add_error('recipient', 'User does not exist')
    else:
        form = MessageForm()
    return render(request, 'messaging/compose.html', {'form': form})

@login_required
def message_detail(request, message_id):
    message = Message.objects.get(id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/message_detail.html', {'message': message})