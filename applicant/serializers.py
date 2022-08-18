from rest_framework import serializers

from .models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source='department.name', read_only=True)
    designation = serializers.CharField(
        source='designation.name', read_only=True)

    class Meta:
        model = Applicant
        fields = [
            'id', 'applicant_id', 'first_name', 'last_name', 'other_name', 'email', 'phone',
            'resuming_date', 'full_name', 'department', 'department_id', 'designation', 'designation_id',
            'status', 'cv_exists', 'comment', 'address', 'salary',
        ]


class AcceptanceSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    designation = serializers.CharField(source='designation.name')
    net_month_salary = serializers.CharField(
        source='applicant_salary')

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
            'designation', 'status', 'net_month_salary', 'snnit_amount', 'snnit_amount_company',
            'provedent_amont', 'provedent_amont_company', 'reports_to',

        ]
