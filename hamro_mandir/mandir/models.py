from django.db import models
from django.contrib.auth.models import User

class Committee(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Committee'
        verbose_name_plural = 'Committees'

    def __str__(self):
        return self.name

class CommitteeMember(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    position = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(upload_to='committee_members/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'

    def __str__(self):
        return f"{self.name} - {self.post}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/', verbose_name='तस्विर')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'कार्यक्रम तस्विर'
        verbose_name_plural = 'कार्यक्रम तस्विरहरू'

    def __str__(self):
        return f"Image for {self.event.title}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='notice_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

class Donor(models.Model):
    name = models.CharField(max_length=100, verbose_name='नाम')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='रकम')
    purpose = models.CharField(max_length=200, verbose_name='उद्देश्य')
    donation_date = models.DateField(verbose_name='दान मिति')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='फोन नम्बर')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='ठेगाना')
    remarks = models.TextField(blank=True, null=True, verbose_name='टिप्पणी')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-donation_date']
        verbose_name = 'दाता'
        verbose_name_plural = 'दाताहरू'

    def __str__(self):
        return f"{self.name} - Rs. {self.amount}"

class MissionVision(models.Model):
    TYPES = [
        ('mission', 'Mission'),
        ('vision', 'Vision')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mission Vision'
        verbose_name_plural = 'Mission Vision'

    def __str__(self):
        return f"{self.category}: {self.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"
