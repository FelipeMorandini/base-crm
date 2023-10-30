from .models import Record
from .forms import SignUpForm, AddRecordForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def home(request):
    records = Record.objects.all()
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('home')
    
    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data['username']
          password = form.cleaned_data['password1']
          user = authenticate(username=username, password=password)
          login(request, user)
          messages.success(request, 'You have successfully registered!')
          return redirect('home')
    
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        return render(request, 'record.html', {'record': record})
    else:
        messages.error(request, 'You must be logged in to view that page!')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        record.delete()
        messages.success(request, 'Record was deleted successfully!')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete a record!')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record was added successfully!')
                return redirect('home')
        else:
            return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to add a record!')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record was updated successfully!')
                return redirect('home')
        else:
            return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to update a record!')
        return redirect('home')