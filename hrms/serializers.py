from dataclasses import fields

from rest_framework import serializers

from .models import (Dependant, Education, Employee, Leave,
                     ProfessionalMembership,Documente)





class EmployeeSerializer(serializers.ModelSerializer):
    # profile_exists = serializers.CharField('profile_exists')
    # designation_name = serializers.CharField(source='designation')
    department = serializers.CharField(source='department.name')
    # department = serializers.CharField(source='employee.department')



    class Meta:
        model = Employee
        fields = ['pk', 'employee_id', 'is_head','full_name', 'emp_uiid', 'status','is_merried', 'date_employed',
                  'mobile', 'email', 'address', 'profile_exists', 'with_beneficiary', 'department',]


class GetEmployeeSerializer(serializers.ModelSerializer):
    # cv_exists = serializers.URLField(source='applicant.cv_exists')

    class Meta:
        model = Employee
        fields = ['pk', 'employee_id', 'title', 'full_name', 'first_name',
                  'last_name', 'is_head', 'nia', 'other_name', 'status', 'date_employed',
                  'other_name', 'mobile', 'email', 'address',
                  'profile_exists', 'with_beneficiary', 'department',
                  'dob', 'age', 'languages', 'place_of_birth', 'nationality', 'country', 'gender',
                   'snnit_number','is_merried', 'designation', 'bank_branch', 'bank_name', 'bank_ac', 
                   'salary', 'emergency_name','emergency_phone', 'emergency_address', 'next_of_kin_name', 
                   'next_of_kin_phone', 'next_of_kin_address', 'next_of_kin_relationship', 'my_group',
                   'applicant_cv_exists','exit_check','date_exited',
                  ]



class DocumentSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='filename')
    category_id = serializers.CharField(source='filename.pk')


    class Meta:
        model = Documente
        fields = ['pk','category_id','category','description','file','date']



class LeaveSerializer(serializers.ModelSerializer):
    handle_over_to = serializers.CharField(source='handle_over_to.full_name')
    handle_over_to_pk = serializers.CharField(source='handle_over_to.pk')
    employee_id = serializers.CharField(source='employee.employee_id')
    group = serializers.CharField(source='employee.my_group')
    employee__name = serializers.CharField(source='employee.full_name')
    department = serializers.CharField(source='employee.department')
    employee_id = serializers.CharField(source='employee.employee_id')

    policy = serializers.CharField(source='policy.name')
    policy_id = serializers.CharField(source='policy.pk')

    class Meta:
        model = Leave
        fields = [
            'id', 'handle_over_to', 'handle_over_to_pk',
            'employee_id', 'group', 'policy', 'policy_id', 'created_at',
            'start', 'end', 'status', 'phone', 'resuming_date', 'file',
            'collegue_approve', 'line_manager', 'hr_manager', 'from_leave', 'employee',
            'employee__name', 'department', 'employee_id','leavedays'

        ]
        # fields = '__all__'
