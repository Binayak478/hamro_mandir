import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Committee(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    number_of_positions = models.IntegerField(default=0, verbose_name='Number of Positions')
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
    
    def delete(self, *args, **kwargs):
        """Delete the image file from storage when the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        # Automatically delete images when a GalleryImage instance is deleted
@receiver(models.signals.post_delete, sender=CommitteeMember)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Deletes the file from filesystem when the model instance is deleted."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.title}"
    
    def delete(self, *args, **kwargs):
        """Delete the image file from storage when the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        # Automatically delete images when a GalleryImage instance is deleted
@receiver(models.signals.post_delete, sender=EventImage)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Deletes the file from filesystem when the model instance is deleted."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='notice_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        """Delete the image file from storage when the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        # Automatically delete images when a GalleryImage instance is deleted
@receiver(models.signals.post_delete, sender=Notice)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Deletes the file from filesystem when the model instance is deleted."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)

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
    
    def delete(self, *args, **kwargs):
        """Delete the image file from storage when the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        # Automatically delete images when a GalleryImage instance is deleted
@receiver(models.signals.post_delete, sender=Blog)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Deletes the file from filesystem when the model instance is deleted."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)
    

class BeaDonor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='रकम')
    image = models.ImageField(upload_to='be_a_donor_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'BeaDonor'
        verbose_name_plural = 'BeaDonors'

    def __str__(self):
        return f"{self.name} - {self.subject}"   

class Donor(models.Model):
    name = models.CharField(max_length=100, verbose_name='नाम')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='रकम')
    purpose = models.CharField(max_length=200, verbose_name='उद्देश्य')
    donation_date = models.DateField(verbose_name='दान मिति')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='फोन नम्बर')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='ठेगाना')
    remarks = models.TextField(blank=True, null=True, verbose_name='टिप्पणी')
    image = models.ImageField(upload_to='donor_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-donation_date']
        verbose_name = 'दाता'
        verbose_name_plural = 'दाताहरू'

    def __str__(self):
        return f"{self.name} - Rs. {self.amount}"
    
    def delete(self, *args, **kwargs):
        """Delete the image file from storage when the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        # Automatically delete images when a GalleryImage instance is deleted
@receiver(models.signals.post_delete, sender=Donor)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """Deletes the file from filesystem when the model instance is deleted."""
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)

class MissionVision(models.Model):
    TYPE_CHOICES = [
        ('mission', 'लक्ष्य'),
        ('vision', 'दृष्टि')
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    point = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['type', 'order']
        db_table = 'mandir_missionvision'  # explicitly set table name

    def __str__(self):
        return f"{self.get_type_display()} Point {self.order}"

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

class About(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Balance(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Balance: रु. {self.amount} ({self.created_at})"
    
def save(self, *args, **kwargs):
    # Get the latest balance
    latest_balance = Balance.objects.first()
    if not latest_balance and self.transaction_type == 'expense':
        raise ValidationError("Cannot record expense without initial balance")

    current_balance = latest_balance.amount if latest_balance else 0
    
    # Calculate new balance
    if self.transaction_type == 'income':
        new_balance = current_balance + self.amount
    else:  # expense
        if current_balance < self.amount:
            raise ValidationError("Insufficient balance for this expense")
        new_balance = current_balance - self.amount

    # Create new balance record
    Balance.objects.create(
        amount=new_balance,
        remarks=f"{self.get_transaction_type_display()}: {self.description[:50]}"
    )

    super().save(*args, **kwargs)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'आम्दानी'),
        ('expense', 'खर्च'),
    )

    CATEGORIES = (
        ('donation', 'दान'),
        ('puja', 'पूजा'),
        ('maintenance', 'मर्मत'),
        ('salary', 'तलब'),
        ('utilities', 'उपयोगिता'),
        ('other', 'अन्य'),
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    date = models.DateField()
    description = models.TextField()
    receipt_no = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()}: रु.{self.amount} - {self.description[:30]}"

    def save(self, *args, **kwargs):
        # Get the latest balance
        latest_balance = Balance.objects.first()
        if not latest_balance and self.transaction_type == 'expense':
            raise ValidationError("Cannot record expense without initial balance")

        current_balance = latest_balance.amount if latest_balance else 0
        
        # Calculate new balance
        if self.transaction_type == 'income':
            new_balance = current_balance + self.amount
        else:  # expense
            if current_balance < self.amount:
                raise ValidationError("Insufficient balance for this expense")
            new_balance = current_balance - self.amount

        # Create new balance record
        Balance.objects.create(
            amount=new_balance,
            remarks=f"After {self.get_transaction_type_display()}: {self.description[:50]}"
        )

        super().save(*args, **kwargs)
