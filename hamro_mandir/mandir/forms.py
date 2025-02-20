from django import forms
from django.forms import inlineformset_factory
from .models import Event, EventImage, Notice, Blog, Committee, CommitteeMember, Donor, Contact, About, MissionVision

class EventForm(forms.ModelForm):
    event_year = forms.IntegerField(min_value=1900, max_value=2100)
    event_month = forms.IntegerField(min_value=1, max_value=12)
    event_day = forms.IntegerField(min_value=1, max_value=31)
    event_hour = forms.IntegerField(min_value=0, max_value=23)
    event_minute = forms.IntegerField(min_value=0, max_value=59)

    class Meta:
        model = Event
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'rows': 4
        })
        for field in ['event_year', 'event_month', 'event_day', 'event_hour', 'event_minute']:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
            })

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
        })

EventImageFormSet = inlineformset_factory(
    Event,
    EventImage,
    form=EventImageForm,
    extra=3,
    can_delete=True,
    max_num=10
)

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'description':
                self.fields[field].widget = forms.Textarea(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
                    'rows': 6
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
                })

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'description':
                self.fields[field].widget = forms.Textarea(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
                    'rows': 6
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
                })

class CommitteeForm(forms.ModelForm):
    start_year = forms.IntegerField(min_value=1900, max_value=2100)
    start_month = forms.IntegerField(min_value=1, max_value=12)
    start_day = forms.IntegerField(min_value=1, max_value=31)
    
    end_year = forms.IntegerField(min_value=1900, max_value=2100, required=False)
    end_month = forms.IntegerField(min_value=1, max_value=12, required=False)
    end_day = forms.IntegerField(min_value=1, max_value=31, required=False)

    class Meta:
        model = Committee
        fields = ['name', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
        })
        for field in ['start_year', 'start_month', 'start_day', 'end_year', 'end_month', 'end_day']:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
            })

class CommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = CommitteeMember
        fields = ['name', 'post', 'position', 'phone_number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
            })

class DonorForm(forms.ModelForm):
    donation_year = forms.IntegerField(min_value=1900, max_value=2100)
    donation_month = forms.IntegerField(min_value=1, max_value=12)
    donation_day = forms.IntegerField(min_value=1, max_value=31)

    class Meta:
        model = Donor
        fields = ['name', 'amount', 'purpose', 'phone', 'address', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'remarks':
                self.fields[field].widget = forms.Textarea(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
                    'rows': 3
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
                })

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'message':
                self.fields[field].widget = forms.Textarea(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
                    'rows': 4
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
                })

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'description':
                self.fields[field].widget = forms.Textarea(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
                    'rows': 6
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
                })

class MissionVisionForm(forms.ModelForm):
    class Meta:
        model = MissionVision
        fields = ['type', 'point', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
        })
        self.fields['point'].widget = forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'rows': 3
        })
        self.fields['order'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
        }) 