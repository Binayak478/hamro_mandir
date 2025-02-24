from django.contrib import admin
from .models import Event, EventImage, Notice, Blog, Committee, CommitteeMember, Donor, Contact,BeaDonor

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('event_date', 'created_at')
    inlines = [EventImageInline]

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'user')

class CommitteeMemberInline(admin.TabularInline):
    model = CommitteeMember
    extra = 1

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    search_fields = ('name',)
    list_filter = ('is_current',)
    inlines = [CommitteeMemberInline]

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'committee', 'position')
    search_fields = ('name', 'post')
    list_filter = ('committee',)

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'purpose', 'donation_date')
    search_fields = ('name', 'purpose')
    list_filter = ('donation_date',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return False  # Prevent adding contacts through admin
    

@admin.register(BeaDonor)
class BeaDonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'amount', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone']

    def has_add_permission(self, request):
        return False  # admin le add garna didaina