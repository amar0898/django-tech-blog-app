from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.db.models import Max


def home(request):
    post=Post.objects.all()
    context = {'posts': post}
    return render(request, 'home/home.html',context)


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        if len(name) < 4 or len(email) < 10 or len(phone) < 10 or len(message) < 5 :
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        post = Post.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains=query)
        postAuthor = Post.objects.filter(author__icontains=query)
        postContent = Post.objects.filter(content__icontains=query)
        post = postTitle.union(postContent, postAuthor)
    if post.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")

    context = {'posts': post, 'query': query}
    return render(request, 'home/search.html', context)


def signUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) < 8:
            messages.error(request, " Your user name should be atleast of 8 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please Try Again.")
            return redirect('home')
    return HttpResponse("404 - Not Found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
