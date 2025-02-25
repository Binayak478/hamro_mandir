from django import forms
from django.forms import inlineformset_factory
from .models import Event, EventImage, Notice, Blog, Committee, CommitteeMember, Donor, Contact, About, MissionVision, Transaction, Balance,BeaDonor

class EventForm(forms.ModelForm):
    event_year = forms.IntegerField(required=True)
    event_month = forms.IntegerField(required=True)
    event_day = forms.IntegerField(required=True)

    class Meta:
        model = Event
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'required': True
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'rows': 4,
            'required': True
        })

    def clean(self):
        cleaned_data = super().clean()
        # We don't need to validate date fields here as they're handled in the view
        return cleaned_data

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
        fields = ['title', 'description', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }

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
                    'rows': 10
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
    
    number_of_positions = forms.IntegerField(min_value=0, required=True, label='Number of Positions')

    class Meta:
        model = Committee
        fields = ['name', 'is_current', 'number_of_positions']

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
    position = forms.ChoiceField(choices=[], label='Position')

    class Meta:
        model = CommitteeMember
        fields = ['name', 'post', 'position', 'phone_number', 'image']

    def __init__(self, committee=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.committee = committee
        if committee:
            self.fields['position'].choices = [(i, i) for i in range(1, committee.number_of_positions + 1)]
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500'
            })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.committee:
            instance.committee = self.committee
        if commit:
            instance.save()
        return instance

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'address', 'phone', 'amount', 'donation_date', 'purpose', 'remarks', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'दाताको नाम',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'ठेगाना'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'फोन नम्बर'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'रकम',
                'required': True
            }),
            'donation_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'type': 'date',
                'required': True
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'दानको उद्देश्य'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'अन्य विवरण',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500'
            })
        }
        labels = {
            'name': 'दाताको नाम *',
            'address': 'ठेगाना',
            'phone': 'फोन नम्बर',
            'amount': 'रकम *',
            'donation_date': 'दान मिति *',
            'purpose': 'दानको उद्देश्य',
            'remarks': 'अन्य विवरण',
            'image': 'तस्विर'
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('तस्विर साइज 5MB भन्दा कम हुनुपर्छ')
        return image

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

class BeaDonorForm(forms.ModelForm):
    class Meta:
        model = BeaDonor
        fields = ['name', 'email', 'phone', 'amount', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 5}),
        }
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
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'required': True
        })
        self.fields['point'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'rows': 4,
            'required': True
        })
        self.fields['order'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500',
            'type': 'number',
            'min': '0',
            'required': True
        })
        
        # Customize field labels
        self.fields['type'].label = 'प्रकार'
        self.fields['point'].label = 'बुँदा'
        self.fields['order'].label = 'क्रम'
        
        # Customize type choices
        self.fields['type'].choices = [
            ('mission', 'लक्ष्य'),
            ('vision', 'दृष्टि')
        ]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'category', 'description', 'receipt_no']
        # Exclude date and created_by as we handle them separately
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling to form fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full p-2 border rounded focus:ring-2 focus:ring-orange-500 focus:border-orange-500'
            })
        
        # Add Nepali labels
        self.fields['transaction_type'].label = 'कारोबारको प्रकार'
        self.fields['amount'].label = 'रकम'
        self.fields['category'].label = 'वर्गीकरण'
        self.fields['description'].label = 'विवरण'
        self.fields['receipt_no'].label = 'रसिद नं.'

class InitialBalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['amount', 'remarks']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'placeholder': 'प्रारम्भिक रकम राख्नुहोस्',
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500',
                'rows': 3,
                'placeholder': 'टिप्पणी लेख्नुहोस्',
            }),
        }
        labels = {
            'amount': 'प्रारम्भिक रकम',
            'remarks': 'टिप्पणी',
        }