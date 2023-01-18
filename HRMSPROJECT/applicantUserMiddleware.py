from django.shortcuts import redirect, reverse
import re
# class ApplicantUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if  request.user.is_applicant ==True:
#                 return redirect('hrms:register_employee')

#             if request.user.is_applicant ==False:
#                 pass

#         response = self.get_response(request)
#         return response


def serach_any(string):
    return re.search(r'[a-zA-Z]',string)

class ApplicantUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
          
            if request.user.is_applicant and request.path != reverse('back_office'):
                return redirect('login')

        response = self.get_response(request)
        return response


# class ActiveUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if not request.user.is_active:
#                 if not request.session.get('redirected',False):
#                     request.session['redirected'] = True
#                     return redirect('account_inactive')

#         response = self.get_response(request)
#         return response
