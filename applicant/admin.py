from django.contrib import admin
from . models import Applicant,OfferLetter,ApplicantOfferLeter
# Register your models here.


class ApplicantOfferLeterInline(admin.TabularInline):
    model = ApplicantOfferLeter


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['applicant_id','full_name','email','phone','department','designation','status','resuming_date','is_applicant']
    search_fields = ('applicant_id','first_name','last_name','other_name','email','phone','department__name','designation__name')
    list_filter = ['department','designation','status','resuming_date']
    inlines = [ApplicantOfferLeterInline]

    

@admin.register(OfferLetter)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['pk','content']
    list_editable = ['content']
    # list_display_links =['pk']

    def has_add_permission(self, request):
            # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and OfferLetter.objects.exists():
            retVal = False
        return retVal
