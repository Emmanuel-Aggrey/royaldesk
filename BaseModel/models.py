from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel, models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    shortname = models.CharField(max_length=5, null=True, blank=True)
    for_management = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("hrms:dept_detail", kwargs={"pk": self.pk})


class Designation(BaseModel, models.Model):
    name = models.CharField(max_length=70)
    # description = models.TextField(max_length=1000,n3ull=True,blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')
    net_month_salary = models.PositiveIntegerField(null=True, blank=True)
    snnit_amount = models.DecimalField(null=True, blank=True, default=5.5,
                                       decimal_places=2, max_digits=5, help_text='value in percentage eg 5.5%')
    snnit_amount_company = models.DecimalField(
        null=True, blank=True, default=13, decimal_places=2, max_digits=5, help_text='value in percentage eg 13%')
    provedent_amont = models.DecimalField(
        null=True, blank=True, default=5, decimal_places=2, max_digits=5, help_text='value in percentage eg 5%')
    provedent_amont_company = models.DecimalField(
        null=True, blank=True, default=5, decimal_places=2, max_digits=5, help_text='value in percentage eg 5%')
    report_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='reports_to') #limit_choices_to={'is_head': True}

    def __str__(self):
        return f'{self.department.name} |  {self.name}' 

    def limit_choices(self):
        return self.pk

    # def get_absolute_url(self):
    #     return reverse("hrms:dept_detail", kwargs={"pk": self.pk})