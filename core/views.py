from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.urls import reverse
from .models import User, Post, Response, EmailConfirmation, CategorySubscription
from .forms import UserRegistrationForm, PostForm, ResponseForm, SubscriptionForm
import uuid

# -----------------------------
# Авторизация
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('news_list')
        else:
            return render(request, 'core/login.html', {'error': 'Неверные данные'})
    return render(request, 'core/login.html')

def logout_user(request):
    logout(request)
    return redirect('news_list')

# -----------------------------
# Новости с пагинацией
def news_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/news_list.html', {'page_obj': page_obj})

# -----------------------------
# Полный пост
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'core/post_detail.html', {'post': post})

# -----------------------------
# Регистрация с подтверждением e-mail
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            token_obj = EmailConfirmation.objects.create(user=user)
            confirm_url = request.build_absolute_uri(reverse('confirm_email', args=[token_obj.token]))
            send_mail(
                'Подтверждение e-mail',
                f'Привет! Подтверди регистрацию: {confirm_url}',
                'noreply@mmorpgboard.com',
                [user.email],
                fail_silently=False
            )
            return render(request, 'core/registration_done.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def confirm_email(request, token):
    obj = get_object_or_404(EmailConfirmation, token=token)
    obj.user.email_confirmed = True
    obj.user.save()
    obj.delete()
    return render(request, 'core/email_confirmed.html')

# -----------------------------
# Создание поста
@login_required
def create_post(request):
    if not request.user.email_confirmed:
        return redirect('register')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('my_posts')
    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form})

@login_required
def my_posts(request):
    posts = request.user.posts.all()
    return render(request, 'core/my_posts.html', {'posts': posts})

# -----------------------------
# Отклики
@login_required
def create_response(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
            send_mail(
                'Новый отклик на ваше объявление',
                f'Пользователь {request.user.username} оставил отклик на "{post.title}"',
                'noreply@mmorpgboard.com',
                [post.author.email],
                fail_silently=False
            )
            return redirect('news_list')
    else:
        form = ResponseForm()
    return render(request, 'core/response_form.html', {'form': form, 'post': post})

@login_required
def manage_responses(request):
    responses = Response.objects.filter(post__author=request.user)
    return render(request, 'core/manage_responses.html', {'responses': responses})

@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, post__author=request.user)
    response.accepted = True
    response.save()
    send_mail(
        'Ваш отклик принят!',
        f'Ваш отклик на "{response.post.title}" принят автором.',
        'noreply@mmorpgboard.com',
        [response.author.email],
        fail_silently=False
    )
    return redirect('manage_responses')

@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, post__author=request.user)
    response.delete()
    return redirect('manage_responses')

# -----------------------------
# Подписка на категории
@login_required
def subscribe_category(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            CategorySubscription.objects.get_or_create(
                user=request.user,
                category=form.cleaned_data['category']
            )
            return redirect('news_list')
    else:
        form = SubscriptionForm()
    return render(request, 'core/subscribe.html', {'form': form})
