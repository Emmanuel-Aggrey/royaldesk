from django.contrib import admin
from .models import User,Helpdesk,Issue,Department,Ticket_Comment
from django.http import HttpResponse
import csv

# Register your models here.



def export_users(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    rows = ['First Name', 'Last Name', 'Department', 'Designation','Head']
    writer.writerow(rows)
    users = queryset.values_list('first_name', 'last_name', 'department__name', 'designation__name', 'is_head',)
    for users in users:
        writer.writerow(users)
    return response


export_users.short_description = 'Export to csv'

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','department','designation','is_head',]
    list_editable = ['is_head']
    list_filter = ['is_head', 'department', 'designation']
    actions = [export_users]




class CommentInline(admin.TabularInline):
    model = Ticket_Comment


class HelpdeskAdmin(admin.ModelAdmin):
    list_display = ['user','subject','status','department','issue','ticket_number','handle_over_to','date']
    list_filter = ['status','department','issue',]
    search_fields = ['ticket_number','handle_over_to__username','user__username']
    inlines = [
        CommentInline,
    ]


admin.site.register(Helpdesk, HelpdeskAdmin)


@admin.register(Issue)
class IssuesAdmin(admin.ModelAdmin):
    pass

