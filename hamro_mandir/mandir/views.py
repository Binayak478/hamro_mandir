from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Notice, CommitteeMember, Committee, Contact, Blog, Donor, EventImage, About, MissionVision
from .forms import (
    EventForm, EventImageFormSet, 
    NoticeForm, BlogForm, 
    CommitteeForm, CommitteeMemberForm,
    DonorForm, ContactForm,
    AboutForm, MissionVisionForm
)
from .decorators import admin_required
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
import pytz
from nepali_datetime import date as nepali_date
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# herne matra
def home(request):
    context = {
        'latest_events': Event.objects.order_by('-event_date')[:3],
        'latest_notices': Notice.objects.order_by('-created_at')[:4],
        'current_committee': Committee.objects.filter(is_current=True).first(),
        'latest_blogs': Blog.objects.order_by('-created_at')[:3],
    }
    return render(request, 'mandir/home.html', context)

def event_list(request):
    events = Event.objects.order_by('-event_date')
    return render(request, 'mandir/events.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'mandir/event_detail.html', {'event': event})

def notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'mandir/notices.html', {'notices': notices})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'mandir/notice_detail.html', {'notice': notice})

def blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'mandir/blog.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'mandir/blog_detail.html', {'blog': blog})

def committee_list(request):
    current_committee = Committee.objects.filter(is_current=True).first()
    past_committees = Committee.objects.filter(is_current=False).order_by('-end_date')
    context = {
        'current_committee': current_committee,
        'past_committees': past_committees,
    }
    return render(request, 'mandir/committee.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'तपाईंको सन्देश सफलतापूर्वक पठाइएको छ।')
            return redirect('mandir:contact')
    else:
        form = ContactForm()
    return render(request, 'mandir/contact.html', {'form': form})

# admin lai sabai operation garxa
@admin_required
def admin_dashboard(request):
    context = {
        'total_events': Event.objects.count(),
        'total_notices': Notice.objects.count(),
        'total_messages': Contact.objects.filter(is_read=False).count(),
        'total_donors': Donor.objects.count(),
        'recent_contacts': Contact.objects.order_by('-created_at')[:5],
    }
    return render(request, 'mandir/admin/dashboard.html', context)


@admin_required
def admin_event_list(request):
    events = Event.objects.order_by('-event_date')
    return render(request, 'mandir/admin/event_list.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        try:
            # Get date components from the form
            year = int(request.POST.get('event_year', 0))
            month = int(request.POST.get('event_month', 0))
            day = int(request.POST.get('event_day', 0))

            # Validate date components
            if not (2000 <= year <= 2100):
                messages.error(request, "कृपया मान्य वर्ष प्रविष्ट गर्नुहोस्")
                return render(request, 'mandir/admin/event_form.html', {'form': form})
            
            if not (1 <= month <= 12):
                messages.error(request, "कृपया मान्य महिना प्रविष्ट गर्नुहोस्")
                return render(request, 'mandir/admin/event_form.html', {'form': form})
            
            if not (1 <= day <= 32):
                messages.error(request, "कृपया मान्य दिन प्रविष्ट गर्नुहोस्")
                return render(request, 'mandir/admin/event_form.html', {'form': form})

            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                
                # Get current time in Nepal timezone
                nepal_tz = pytz.timezone('Asia/Kathmandu')
                current_time = datetime.now(nepal_tz)
                
                try:
                    # Create datetime object with the provided date and current time
                    event_datetime = datetime(
                        year=year,
                        month=month,
                        day=day,
                        hour=current_time.hour,
                        minute=current_time.minute,
                        second=current_time.second,
                        tzinfo=nepal_tz
                    )
                    
                    # Convert to UTC for storage
                    utc_dt = event_datetime.astimezone(pytz.UTC)
                    event.event_date = utc_dt
                    event.save()
                    
                    # Handle images
                    images = request.FILES.getlist('images')
                    for image in images:
                        EventImage.objects.create(event=event, image=image)
                    
                    messages.success(request, 'कार्यक्रम सफलतापूर्वक सिर्जना गरियो')
                    return redirect('mandir:admin_event_list')
                    
                except ValueError as e:
                    messages.error(request, "कृपया मान्य मिति प्रविष्ट गर्नुहोस्")
                    return render(request, 'mandir/admin/event_form.html', {'form': form})
                
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                
        except (ValueError, TypeError) as e:
            messages.error(request, "कृपया सबै मिति फिल्डहरू भर्नुहोस्")
            
    else:
        form = EventForm()
    
    return render(request, 'mandir/admin/event_form.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                
                # Get date components from the form
                year = int(request.POST.get('year'))
                month = int(request.POST.get('month'))
                day = int(request.POST.get('day'))

                # Get current time in Nepal timezone
                nepal_tz = pytz.timezone('Asia/Kathmandu')
                current_time = datetime.now(nepal_tz)
                
                # Create datetime object with the provided date and current time
                event_datetime = datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=current_time.hour,
                    minute=current_time.minute,
                    second=current_time.second,
                    tzinfo=nepal_tz
                )
                
                # Convert to UTC for storage
                utc_dt = event_datetime.astimezone(pytz.UTC)
                event.event_date = utc_dt
                event.save()
                
                # Handle image deletions
                delete_images = request.POST.getlist('delete_images')
                EventImage.objects.filter(id__in=delete_images).delete()
                
                # Handle new images
                images = request.FILES.getlist('images')
                for image in images:
                    EventImage.objects.create(event=event, image=image)
                
                messages.success(request, 'कार्यक्रम सफलतापूर्वक अपडेट गरियो')
                return redirect('mandir:admin_event_list')
                
            except Exception as e:
                print(f"Error updating event: {str(e)}")  # For debugging
                messages.error(request, f"कार्यक्रम अपडेट गर्दा त्रुटि: {str(e)}")
        else:
            print(f"Form errors: {form.errors}")  # For debugging
            messages.error(request, "कृपया फारम सही तरिकाले भर्नुहोस्")
    else:
        form = EventForm(instance=event)
        if event.event_date:
            # Convert UTC to Nepal time for display
            nepal_tz = pytz.timezone('Asia/Kathmandu')
            nepal_dt = event.event_date.astimezone(nepal_tz)
            
            # Convert to Nepali date
            nep_date = nepali_date.from_datetime_date(nepal_dt.date())
            
            # Initialize form with Nepali date
            form.initial.update({
                'year': nep_date.year,
                'month': nep_date.month,
                'day': nep_date.day
            })
    
    return render(request, 'mandir/admin/event_form.html', {'form': form})

@admin_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'कार्यक्रम सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_event_list')
    return render(request, 'mandir/admin/event_confirm_delete.html', {'event': event})

@admin_required
def event_image_delete(request, pk, image_pk):
    event = get_object_or_404(Event, pk=pk)
    image = get_object_or_404(EventImage, pk=image_pk, event=event)
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'तस्विर सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:event_update', pk=pk)
    
    # If it's a GET request, redirect to event update page
    return redirect('mandir:event_update', pk=pk)


@admin_required
def admin_notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'mandir/admin/notice_list.html', {'notices': notices})

@admin_required
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            messages.success(request, 'सूचना सफलतापूर्वक सिर्जना गरियो।')
            return redirect('mandir:admin_notice_list')
    else:
        form = NoticeForm()
    return render(request, 'mandir/admin/notice_form.html', {'form': form})

@admin_required
def notice_update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'सूचना सफलतापूर्वक अपडेट गरियो।')
            return redirect('mandir:admin_notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'mandir/admin/notice_form.html', {'form': form})

@admin_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'सूचना सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_notice_list')
    return render(request, 'mandir/admin/notice_confirm_delete.html', {'notice': notice})


@admin_required
def admin_committee_list(request):
    committees = Committee.objects.order_by('-start_date')
    return render(request, 'mandir/admin/committee_list.html', {'committees': committees})

@admin_required
def committee_create(request):
    if request.method == 'POST':
        form = CommitteeForm(request.POST)
        if form.is_valid():
            committee = form.save(commit=False)
            
            # Handle start date
            try:
                start_year = int(request.POST.get('start_year'))
                start_month = int(request.POST.get('start_month'))
                start_day = int(request.POST.get('start_day'))
                committee.start_date = date(start_year, start_month, start_day)
            except (ValueError, TypeError):
                form.add_error(None, "सुरु मिति अमान्य छ")
                return render(request, 'mandir/admin/committee_form.html', {'form': form})

            # Handle end date (optional)
            try:
                end_year = request.POST.get('end_year')
                end_month = request.POST.get('end_month')
                end_day = request.POST.get('end_day')
                if end_year and end_month and end_day:
                    committee.end_date = date(int(end_year), int(end_month), int(end_day))
                else:
                    committee.end_date = None
            except (ValueError, TypeError):
                form.add_error(None, "अन्त्य मिति अमान्य छ")
                return render(request, 'mandir/admin/committee_form.html', {'form': form})

            if committee.is_current:
                Committee.objects.filter(is_current=True).update(is_current=False)

            committee.save()
            messages.success(request, 'कार्य समिति सफलतापूर्वक सिर्जना गरियो')
            return redirect('mandir:admin_committee_list')
    else:
        form = CommitteeForm()
    
    return render(request, 'mandir/admin/committee_form.html', {'form': form})

@admin_required
def committee_update(request, pk):
    committee = get_object_or_404(Committee, pk=pk)
    if request.method == 'POST':
        form = CommitteeForm(request.POST, instance=committee)
        if form.is_valid():
            committee = form.save(commit=False)
            
#start date ko lagi
            try:
                start_year = int(request.POST.get('start_year'))
                start_month = int(request.POST.get('start_month'))
                start_day = int(request.POST.get('start_day'))
                committee.start_date = date(start_year, start_month, start_day)
            except (ValueError, TypeError):
                form.add_error(None, "सुरु मिति अमान्य छ")
                return render(request, 'mandir/admin/committee_form.html', {'form': form})

#end date ko lagi
            try:
                end_year = request.POST.get('end_year')
                end_month = request.POST.get('end_month')
                end_day = request.POST.get('end_day')
                if end_year and end_month and end_day:
                    committee.end_date = date(int(end_year), int(end_month), int(end_day))
                else:
                    committee.end_date = None
            except (ValueError, TypeError):
                form.add_error(None, "अन्त्य मिति अमान्य छ")
                return render(request, 'mandir/admin/committee_form.html', {'form': form})

            if committee.is_current and not Committee.objects.get(pk=pk).is_current:
                Committee.objects.filter(is_current=True).update(is_current=False)

            committee.save()
            messages.success(request, 'कार्य समिति सफलतापूर्वक अपडेट गरियो')
            return redirect('mandir:admin_committee_list')
    else:
        form = CommitteeForm(instance=committee)
        if committee.start_date:
            form.initial.update({
                'start_year': committee.start_date.year,
                'start_month': committee.start_date.month,
                'start_day': committee.start_date.day,
            })
        if committee.end_date:
            form.initial.update({
                'end_year': committee.end_date.year,
                'end_month': committee.end_date.month,
                'end_day': committee.end_date.day,
            })
    
    return render(request, 'mandir/admin/committee_form.html', {'form': form})

@admin_required
def committee_delete(request, pk):
    committee = get_object_or_404(Committee, pk=pk)
    if request.method == 'POST':
        committee.delete()
        messages.success(request, 'कार्य समिति सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_committee_list')
    return render(request, 'mandir/admin/committee_confirm_delete.html', {'committee': committee})

# Committee Member Admin Views
@admin_required
def committee_member_create(request, committee_pk):
    committee = get_object_or_404(Committee, pk=committee_pk)
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.committee = committee
            member.save()
            messages.success(request, 'समिति सदस्य सफलतापूर्वक थपियो।')
            return redirect('mandir:admin_committee_list')
    else:
        form = CommitteeMemberForm()
    return render(request, 'mandir/admin/committee_member_form.html', {
        'form': form,
        'committee': committee
    })

@admin_required
def committee_member_update(request, pk):
    member = get_object_or_404(CommitteeMember, pk=pk)
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'समिति सदस्य सफलतापूर्वक अपडेट गरियो।')
            return redirect('mandir:admin_committee_list')
    else:
        form = CommitteeMemberForm(instance=member)
    return render(request, 'mandir/admin/committee_member_form.html', {
        'form': form,
        'member': member
    })

@admin_required
def committee_member_delete(request, pk):
    member = get_object_or_404(CommitteeMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'समिति सदस्य सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_committee_list')
    return render(request, 'mandir/admin/committee_member_confirm_delete.html', {'member': member})

# Blog Admin Views
@admin_required
def admin_blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'mandir/admin/blog_list.html', {'blogs': blogs})

@admin_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'ब्लग सफलतापूर्वक सिर्जना गरियो।')
            return redirect('mandir:admin_blog_list')
    else:
        form = BlogForm()
    return render(request, 'mandir/admin/blog_form.html', {'form': form})

@admin_required
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'ब्लग सफलतापूर्वक अपडेट गरियो।')
            return redirect('mandir:admin_blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'mandir/admin/blog_form.html', {'form': form})

@admin_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'ब्लग सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_blog_list')
    return render(request, 'mandir/admin/blog_confirm_delete.html', {'blog': blog})

# Donor Admin Views
@admin_required
def admin_donor_list(request):
    donors = Donor.objects.order_by('-donation_date')
    return render(request, 'mandir/admin/donor_list.html', {'donors': donors})

@admin_required
def donor_create(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'दाता विवरण सफलतापूर्वक थपियो।')
            return redirect('mandir:admin_donor_list')
    else:
        form = DonorForm()
    return render(request, 'mandir/admin/donor_form.html', {'form': form})

@admin_required
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'दाता विवरण सफलतापूर्वक अपडेट गरियो।')
            return redirect('mandir:admin_donor_list')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'mandir/admin/donor_form.html', {'form': form})

@admin_required
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'दाता विवरण सफलतापूर्वक मेटाइयो।')
        return redirect('mandir:admin_donor_list')
    return render(request, 'mandir/admin/donor_confirm_delete.html', {'donor': donor})

# Contact Admin Views
@admin_required
def admin_contact_list(request):
    contacts = Contact.objects.order_by('-created_at')
    return render(request, 'mandir/admin/contact_list.html', {'contacts': contacts})

@admin_required
def contact_detail(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'mandir/admin/contact_detail.html', {'message': message})

@admin_required
def contact_toggle_read(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    message.is_read = not message.is_read
    message.save()
    return redirect('mandir:contact_detail', pk=pk)

@admin_required
def contact_delete(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    message.delete()
    messages.success(request, 'सन्देश सफलतापूर्वक मेटाइयो।')
    return redirect('mandir:admin_contact_list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'सफलतापूर्वक लगइन गरियो')
            return redirect('mandir:admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'mandir/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'सफलतापूर्वक लगआउट गरियो')
    return redirect('mandir:home')

def gallery_view(request):
    # Get events that have images, ordered by event date
    events = Event.objects.filter(images__isnull=False).distinct().order_by('-event_date')
    return render(request, 'mandir/gallery.html', {'events': events})

def about_view(request):
    about = About.objects.first()
    return render(request, 'mandir/about.html', {'about': about})

@login_required
def admin_about_list(request):
    abouts = About.objects.all().order_by('-created_at')
    return render(request, 'mandir/admin/about_list.html', {'abouts': abouts})

@login_required
def about_create(request):
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            about = form.save(commit=False)
            about.user = request.user
            about.save()
            messages.success(request, 'हाम्रो बारेमा सफलतापूर्वक सिर्जना गरियो')
            return redirect('mandir:admin_about_list')
    else:
        form = AboutForm()
    return render(request, 'mandir/admin/about_form.html', {'form': form})

@login_required
def about_update(request, pk):
    about = get_object_or_404(About, pk=pk)
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'हाम्रो बारेमा सफलतापूर्वक अपडेट गरियो')
            return redirect('mandir:admin_about_list')
    else:
        form = AboutForm(instance=about)
    return render(request, 'mandir/admin/about_form.html', {'form': form})

@login_required
def about_delete(request, pk):
    about = get_object_or_404(About, pk=pk)
    about.delete()
    messages.success(request, 'हाम्रो बारेमा सफलतापूर्वक मेटाइयो')
    return redirect('mandir:admin_about_list')

def mission_vision_view(request):
    missions = MissionVision.objects.filter(type='mission')
    visions = MissionVision.objects.filter(type='vision')
    return render(request, 'mandir/mission_vision.html', {
        'missions': missions,
        'visions': visions
    })

@login_required
def admin_mission_vision_list(request):
    missions = MissionVision.objects.filter(type='mission')
    visions = MissionVision.objects.filter(type='vision')
    return render(request, 'mandir/admin/mission_vision_list.html', {
        'missions': missions,
        'visions': visions
    })

@login_required
def mission_vision_create(request):
    if request.method == 'POST':
        form = MissionVisionForm(request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.user = request.user
            point.save()
            messages.success(request, 'बुँदा सफलतापूर्वक सिर्जना गरियो')
            return redirect('mandir:admin_mission_vision_list')
    else:
        form = MissionVisionForm()
    return render(request, 'mandir/admin/mission_vision_form.html', {'form': form})

@login_required
def mission_vision_update(request, pk):
    point = get_object_or_404(MissionVision, pk=pk)
    if request.method == 'POST':
        form = MissionVisionForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            messages.success(request, 'बुँदा सफलतापूर्वक अपडेट गरियो')
            return redirect('mandir:admin_mission_vision_list')
    else:
        form = MissionVisionForm(instance=point)
    return render(request, 'mandir/admin/mission_vision_form.html', {'form': form})

@login_required
def mission_vision_delete(request, pk):
    point = get_object_or_404(MissionVision, pk=pk)
    point.delete()
    messages.success(request, 'बुँदा सफलतापूर्वक मेटाइयो')
    return redirect('mandir:admin_mission_vision_list')

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build password reset URL
            reset_url = request.build_absolute_uri(
                reverse('mandir:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Send email
            subject = "Password Reset Requested"
            email_template_name = "mandir/password_reset_email.html"
            context = {
                "email": user.email,
                'reset_url': reset_url,
                'user': user,
            }
            email_message = render_to_string(email_template_name, context)
            
            send_mail(
                subject,
                email_message,
                'noreply@yoursite.com',  # Change this to your email
                [user.email],
                fail_silently=False
            )
            
            messages.success(request, "पासवर्ड रिसेट लिंक तपाईंको इमेलमा पठाइएको छ।")
            return redirect('mandir:login')
            
        except User.DoesNotExist:
            messages.error(request, "यो इमेल ठेगाना दर्ता गरिएको छैन।")
            
    return render(request, 'mandir/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "तपाईंको पासवर्ड सफलतापूर्वक परिवर्तन गरियो।")
                return redirect('mandir:login')
            else:
                messages.error(request, "पासवर्डहरू मेल खाएनन्।")
        
        return render(request, 'mandir/password_reset_confirm.html')
    else:
        messages.error(request, "पासवर्ड रिसेट लिंक अमान्य छ।")
        return redirect('mandir:login')
