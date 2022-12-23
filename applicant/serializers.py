from rest_framework import serializers

from .models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name', read_only=True)
    designation_name = serializers.CharField(
        source='designation.name', read_only=True)
    applicant_id = serializers.CharField(read_only=True)

    class Meta:
        model = Applicant
        fields = [
            'id', 'applicant_id', 'first_name', 'last_name', 'other_name', 'email', 'phone',
            'resuming_date', 'full_name', 'department','department_name', 'designation', 'designation_name',
            'status', 'cv_exists', 'cv','comment', 'message','address', 'applicant_salary','salary',
        ]


class AcceptanceSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')
    designation = serializers.CharField(source='designation.name')
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
            'provedent_amont', 'provedent_amont_company', 'reports_to','comment',

        ]



class ApplicantOfferLetterSerializer(serializers.ModelSerializer):
    offer_letter = serializers.ListField(child=serializers.FileField())

    class Meta:
        model = Applicant
        fields = ['offer_letter']
            
            

class FileUploadSerializer(serializers.ModelSerializer):        
    file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
        allow_empty_file=False,
        use_url=False ))

    class Meta:
        model = Applicant
        fields = '__all__'

    def create(self, validated_data):
        # name=validated_data['applicant_id']
        file=validated_data.pop('offer_letter')   
        image_list = []     
        for img in file:
            photo=Applicant.objects.create(offer_letter=img)
            imageurl = f'{photo.file.url}'
            image_list.append(imageurl)        
        return image_list


class FileUploadDisplaySerializer(serializers.ModelSerializer):        
    class Meta:
        model = Applicant
        fields = '__all__'
