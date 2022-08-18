from django.contrib import admin
from .models import User,Helpdesk,Issue,Department,Ticket_Comment
# Register your models here.


admin.site.register(User)


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

