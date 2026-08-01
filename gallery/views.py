from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import translation
from django.http import HttpResponseRedirect
from collections import defaultdict
from .models import Photo
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PhotoUploadForm


# ==================== ТІЛ ӨЗГЕРТУ ====================
def set_language(request, lang_code):
    if lang_code in ['kk', 'ru', 'en']:
        translation.activate(lang_code)
        request.session['django_language'] = lang_code
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie('django_language', lang_code, max_age=31536000)
        return response
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ==================== ГАЛЕРЕЯ ====================
@login_required
def gallery(request):
    photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
    
    grouped_photos = defaultdict(list)
    sorted_dates = []
    for photo in photos:
        date_key = photo.uploaded_at.date()
        grouped_photos[date_key].append(photo)
        if date_key not in sorted_dates:
            sorted_dates.append(date_key)
    
    sorted_dates.sort(reverse=True)
    
    context = {
        'photos': photos,
        'grouped_photos': grouped_photos,
        'sorted_dates': sorted_dates,
    }
    return render(request, 'gallery/gallery.html', context)


# ==================== ТІРКЕЛУ ====================
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Тіркелу сәтті!')
            return redirect('gallery')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gallery/register.html', {'form': form})


# ==================== КІРУ ====================
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, f'Қош келдіңіз, {user.username}!')
                return redirect('gallery')
        messages.error(request, 'Қате логин немесе пароль')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'gallery/login.html', {'form': form})


# ==================== ШЫҒУ ====================
def user_logout(request):
    logout(request)
    messages.info(request, 'Сіз шықтыңыз')
    return redirect('login')



# ==================== СУРЕТ ЖҮКТЕУ ====================
@login_required
def upload_photo(request):
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        if not files:
            messages.error(request, 'Ешқандай сурет таңдалмады!')
            return redirect('upload')
        
        count = 0
        for f in files:
            photo = Photo(user=request.user, image=f)
            photo.save()
            count += 1
        
        messages.success(request, f'{count} сурет сәтті жүктелді!')
        return redirect('gallery')
    else:
        form = PhotoUploadForm()
    return render(request, 'gallery/upload.html', {'form': form})
# ==================== СУРЕТТІ ЖОЮ ====================
@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    photo.delete()
    messages.success(request, 'Сурет жойылды!')
    return redirect('gallery')


# ==================== КӨП СУРЕТТІ ЖОЮ ====================
@login_required
def bulk_delete(request):
    if request.method == 'POST':
        photo_ids = request.POST.get('photo_ids', '').split(',')
        photo_ids = [pid for pid in photo_ids if pid.isdigit()]
        if photo_ids:
            Photo.objects.filter(id__in=photo_ids, user=request.user).delete()
            messages.success(request, f'{len(photo_ids)} сурет жойылды!')
        else:
            messages.error(request, 'Ешқандай сурет таңдалмады!')
    return redirect('gallery')