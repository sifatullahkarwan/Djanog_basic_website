from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from  django.contrib.auth.decorators import login_required# it decorator that restricted the user

from django.db.models import Q#Encapsulate filters as objects that can then be combined logically (using & and |).
from django . contrib . auth import authenticate, login,logout

# Create your views here.


from django.contrib.auth.models import User


from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm




# rooms=[
#     {'id':1,'name':'Let\'s learn  python'},{
#      'id':2,'name':'Desgin with me'},{
#      'id':3,'name':'Play with me'},
# ]


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:# it tell us if the user is authenticated it will display the home page
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            usre =User.objects.get(username=username)
        except:
            messages.error(request,'User does\'nt exist')
    
        user = authenticate(request,username=username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'user name or password doesn\'t exist')

    context = {'page':page}
    return render(request,'base/login-register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form =UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username =user.username.lower()# if the user enter upper case it save it like lower case
        user.save()
        login (request,user)
        return redirect('home')
    else:
        messages.error(request,'An erro occoured during registration! ')
    return render(request,'base/login-register.html',{'form':form})

def home(request):# the request is the object of http 
    q = request.GET.get('q')     if request.GET.get('q') !=None else ''
        
#The icontains lookup is used to get records that contains a specified value.
#For a case sensitive search, use the contains lookup.
    rooms=Room.objects.filter(Q(topic__name__icontains = q) |     # show them Room model objects// and resolve the tpic__name to q
     Q(name__icontains = q) |
     Q(description__icontains = q))
    
    topics = Topic.objects.all()
    room_count = rooms.count()# it count the total courses 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains =q))# (Q(room__topic__name__icontains =q)) it fileter the message of specific  brwos topic
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)


def room(request,pk):
    rooms = Room.objects.get(id=pk)# return one single item with unique id
    # room_messages = room.message_set.all()
    # patricipants= room.patricipants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )# it let user to create message
        room.patricipants.add(request.user)# it add the  user when the user add message it will add it in the participant
        return redirect ('room', pk = room.id)
    context = {'rooms':rooms}

    return render(request,'base/room.html',context)# The primary purpose of render() is to take a request, a template, and a dictionary of context data and return an HTTP response with the rendered HTML content. 


def userprofile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)



@login_required(login_url='login')# it means first we should login then do creatRoom function
def creatRoom(request):
    form = RoomForm()
    if request.method == 'POST':#  request.method: A string representing the HTTP method used in the request (e.g., ‘GET’, ‘POST’, ‘PUT’, ‘DELETE’).


        # print(request.POST)# it out the backend like dictionary
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')# redirect = allows you to perform an HTTP redirect. It’s often used in views to redirect users from one URL to another.
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url  = 'login')

def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('your not allowed here!!')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html')

@login_required(login_url ='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('your not allowed user! ')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})




@login_required(login_url ='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('your not allowed user! ')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

