from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm,UserUpdateForm
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from .decorators import user_not_authenticated
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'pages/profile/profile.html', context={'form': form})

    return redirect("homepage")
def homePage(request):
    posts = Post.objects.all().order_by("-postDate")
    return render(request, "pages/home.html", {
        'posts': posts
    })
def UserHomePage(request):
    posts = Post.objects.all().order_by("-postDate")
    return render(request, "pages/home.html", {
        'posts': posts
    })
def addPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "post added")
            return redirect("homePage")
    else:
        form = PostForm()

    return render(request, "pages/add-post.html", {
        'form': form
    })

def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post-detail.html', {
        'post': post
})

def postDelete(request, pk):
    post = Post.objects.all().get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect("homePage")

    return render(request, "pages/delete-post.html", {
        'post': post
    })
def editPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('postDetail', pk=post.pk)

    return render(request, 'pages/edit-post.html', {
        'post': post,
        'form': form
    })
@user_not_authenticated
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'pages/account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'pages/account/register.html', {'user_form': user_form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homePage")
@user_not_authenticated
def user_login(request):
    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect('homePage')

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "Пожалуйста, пройдите проверку reCaptcha")
                    continue
                messages.error(request, error)

    form = LoginForm()

    return render(
        request=request,
        template_name="pages/account/login.html",
        context={'form': form}
    )