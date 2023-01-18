from rest_framework import serializers

from .models import Applicant,ApplicantOfferLeter

class ApplicantOfferLeterSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicantOfferLeter
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    applicant_offer_letters = ApplicantOfferLeterSerializers(read_only=True,many=True)
    department_name = serializers.CharField(
        source='department.name', read_only=True)
    designation_name = serializers.CharField(
        source='designation.name', read_only=True)
    applicant_id = serializers.CharField(read_only=True)
    user  = serializers.CharField(read_only=True)
    applicant = serializers.BooleanField(help_text='is applciant',read_only=True,source='is_applicant')

    class Meta:
        model = Applicant
        fields = [
            'id', 'applicant_id', 'employee_uuid','user','first_name', 'last_name', 'other_name','applicant', 'email', 'phone',
            'resuming_date', 'full_name', 'department','department_name', 'designation', 'designation_name',
            'status', 'cv_exists', 'cv','comment', 'message','address', 'applicant_salary','salary','applicant_offer_letters',
        ]


class AcceptanceSerializer(serializers.ModelSerializer):
    applicant_offer_letters =ApplicantOfferLeterSerializers(read_only=True,many=True)
    department = serializers.CharField(source='department.name')
    designation = serializers.CharField(source='designation.name')
    offer_letter =ApplicantOfferLeterSerializers(read_only=True,many=True)

    # net_month_salary = serializers.CharField(
    #     source='applicant_salary')

    snnit_amount = serializers.CharField(source='designation.snnit_amount')

    snnit_amount_company = serializers.CharField(
        source='designation.snnit_amount_company')

    provedent_amont = serializers.CharField(
        source='designation.provedent_amont')
    provedent_amont_company = serializers.CharField(
        source='designation.provedent_amont_company')

    reports_to = serializers.CharField(
        source='designation.report_to.name')

    class Meta:
        model = Applicant
        fields = [
            'applicant_id', 'first_name', 'last_name', 'other_name', 'full_name', 'address',
            'email', 'phone', 'resuming_date', 'full_name', 'department',
            'designation', 'status', 'applicant_salary', 'snnit_amount', 'snnit_amount_company',
            'provedent_amont', 'provedent_amont_company', 'reports_to','comment','applicant_offer_letters',

        ]


class ApplicantOfferLetterSerializer(serializers.ModelSerializer):
    applicant_id = serializers.CharField(read_only=True)
    offer_letter = serializers.ListField(child=serializers.FileField())

    class Meta:
        model = Applicant
        fields = ['applicant_id','offer_letter']
            
            



