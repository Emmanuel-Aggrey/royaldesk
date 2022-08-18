from dataclasses import fields
from rest_framework import serializers
from .models import Issue,Helpdesk


class HelpdeskSerializer(serializers.ModelSerializer):
    # handle_over_to = serializers.CharField(source='handle_over_to')
    issue = serializers.CharField(source='issue.issue_name')
    department = serializers.CharField(source='issue.department.name')
    # handle_over_to_id= serializers.CharField(source='handle_over_to.pk')
    # user_type= serializers.CharField(source='user.user_type')

    


    # policy = serializers.CharField(source='policy.name')
    # policy_id = serializers.CharField(source='policy.pk')

    class Meta:
        model = Helpdesk
        fields = '__all__'