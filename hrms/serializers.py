from dataclasses import fields

from rest_framework import serializers

from applicant.serializers import ApplicantOfferLeterSerializers

from .models import (Dependant, Documente, Education, Employee, Leave,
                     PreviousEployment, ProfessionalMembership, EmployeeExit, RequestChange)


class AllEmployeeSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(read_only=True)
    department_name = serializers.CharField(
        source='department.name', read_only=True)

    designation_name = serializers.CharField(
        source='designation.name', read_only=True)
    exit_check = serializers.CharField(read_only=True)
    date_exited = serializers.CharField(read_only=True)
    pk = serializers.CharField(read_only=True)
    emp_uiid = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_normal_user = serializers.BooleanField(
        source='user.is_normal_user', read_only=True)
    is_applicant = serializers.BooleanField(
        source='user.is_applicant', read_only=True)

    class Meta:
        model = Employee

        fields = [
            'employee_id', 'full_name', 'first_name', 'last_name', 'title', 'gender', 'mobile', 'email', 'dob',
            'other_name', 'is_head', 'salary', 'nia', 'emergency_name', 'emergency_phone',
            'emergency_address', 'place_of_birth', 'is_merried', 'nationality',
            'languages', 'country', 'department', 'designation', 'snnit_number',
            'bank_name', 'bank_branch', 'bank_ac', 'next_of_kin_name', 'next_of_kin_phone',
            'next_of_kin_address', 'next_of_kin_relationship', 'date_employed',
            'address', 'applicant_id', 'anviz_id', 'profile', 'department_name', 'designation_name',
            'exit_check', 'date_exited', 'pk', 'emp_uiid', 'status',
            'profile_exists', 'applicant_cv_exists', 'with_beneficiary', 'is_normal_user', 'registed_employee', 'is_applicant', 'request_change',
            'request_changes_state',
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    # profile_exists = serializers.CharField('profile_exists')
    designation = serializers.CharField(source='designation.name')
    department = serializers.CharField(source='department.name')
    # department = serializers.CharField(source='employee.department')

    class Meta:
        model = Employee
        fields = ['pk', 'employee_id', 'is_head', 'full_name', 'emp_uiid', 'status', 'is_merried', 'gender','date_employed',
                  'mobile', 'email', 'address', 'profile_exists', 'with_beneficiary', 'department','designation' ]


# class ExitEployeeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Employee
#         fields = ['full_name','employement_length','position']

class EmployeeExitSerializer(serializers.ModelSerializer):
    # employee_exit = ExitEployeeSerializer(read_only=True)
    employee_name = serializers.CharField(
        source='employee.full_name', read_only=True)
    employement_length = serializers.CharField(
        source='employee.employement_length', read_only=True)
    position = serializers.CharField(
        source='employee.position', read_only=True)
    status = serializers.CharField(source='employee.status', read_only=True)
    employee = serializers.CharField(read_only=True)

    # name = serializers.JSONField()

    class Meta:
        model = EmployeeExit
        fields = ['employee', 'data', 'employee_name',
                  'employement_length', 'position', 'status']


class DependantSerializer(serializers.ModelSerializer):
    # employee = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(
        source='employee.emp_uiid', read_only=True)

    class Meta:
        model = Dependant
        fields = ['id', 'employee_id', 'gender', 'first_name', 'last_name', 'full_name',
                  'other_name', 'dob', 'mobile', 'address', 'relation', 'is_beneficiary']


class EducationSerializer(serializers.ModelSerializer):
    # employee = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(
        source='employee.emp_uiid', read_only=True)

    class Meta:
        model = Education
        fields = ['id', 'employee_id', 'school_name', 'course', 'certificate',
                  'date_completed']


class PreviousMembershipSerializer(serializers.ModelSerializer):
    # employee = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(
        source='employee.emp_uiid', read_only=True)

    class Meta:
        model = ProfessionalMembership
        fields = ['id', 'employee_id', 'name', 'document']


class PreviousEploymentSerializer(serializers.ModelSerializer):
    # employee = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(
        source='employee.emp_uiid', read_only=True)

    class Meta:
        model = PreviousEployment
        fields = ['id', 'employee_id', 'company', 'job_title', 'date']


class DocumentSerializer(serializers.ModelSerializer):
    offer_letter = ApplicantOfferLeterSerializers(
        source='employee.applicant.applicant_offer_letters', read_only=True, many=True)

    # cv = serializers.CharField(source='employee.applicant.cv.url')
    category = serializers.CharField(source='filename')
    category = serializers.CharField(source='filename')
    category_id = serializers.CharField(source='filename.pk')
    employee = serializers.CharField(
        source='employee.employee_id', read_only=True)

    class Meta:
        model = Documente
        fields = ['employee', 'pk', 'category_id', 'category',
                  'description', 'file', 'date', 'offer_letter', ]


class LeaveSerializer(serializers.ModelSerializer):
    # handle_over_to = serializers.CharField(source='handle_over_to.full_name')
    # handle_over_to_pk = serializers.CharField(source='handle_over_to.pk')
    # employee_id = serializers.CharField(source='employee.employee_id')
    group = serializers.CharField(source='employee.my_group')
    employee__name = serializers.CharField(source='employee.full_name')
    department = serializers.CharField(source='employee.department')
    employee_id = serializers.CharField(source='employee.employee_id')
    url = serializers.CharField(source='get_absolute_url')

    policy = serializers.CharField(source='policy.name')
    policy_id = serializers.CharField(source='policy.pk')

    class Meta:
        model = Leave
        fields = [
            'id', 'url', 'employee_id', 'group', 'policy', 'policy_id', 'created_at',
            'start', 'end', 'status', 'phone', 'resuming_date', 'file',
            'supervisor', 'line_manager', 'hr_manager', 'from_leave', 'employee',
            'employee__name', 'department', 'leavedays'

        ]
        # fields = '__all__'


class RequestChangeSerilizer(serializers.ModelSerializer):
    employee = serializers.CharField(
        source='employee.full_name', read_only=True)
    department = serializers.CharField(
        source='employee.department', read_only=True)
    request_change = serializers.BooleanField(source='employee.request_change')

    class Meta:
        model = RequestChange
        fields = ['pk', 'employee', 'department',
                  'status', 'text', 'request_change','created_at']
