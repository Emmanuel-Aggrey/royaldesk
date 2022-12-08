from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.contrib.auth.hashers import check_password
from decouple import config
def not_in_site(user):
    try:
        if user.belongs_to_site:
            return True       #Condition's will come here
        return False
    except:
        pass
   

class SiteRequiredMixin(object):
    """"Custom user passes test Required Mixin"""
    @method_decorator(user_passes_test(not_in_site, login_url='/warehouse_registrations/'))
    def dispatch(self, request, *args, **kwargs):
        return super(SiteRequiredMixin, self).dispatch(request, *args, **kwargs)



def belongs_to_site(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/warehouse_registrations/'):
    '''
    Decorator for views that checks that the logged in user belongs to site,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
    # lambda u: u.is_active and u.is_student or u.is_superuser,  
    lambda user: user.belongs_to_site,
    login_url=login_url,
    redirect_field_name=redirect_field_name
        
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
  
    
   


def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user belongs to site,
    redirects to the log-in page if necessary.
    '''
    
    actual_decorator = user_passes_test(
    # lambda u: u.is_active and u.is_student or u.is_superuser,  
    lambda user: user.is_manager or user.is_superuser,
    login_url=login_url,
    redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator


def hod_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user belongs to site,
    redirects to the log-in page if necessary.
    '''
    
    actual_decorator = user_passes_test(
    # lambda u: u.is_active and u.is_student or u.is_superuser,  
    lambda user: user.is_head or user.is_superuser,
    login_url=login_url,
    redirect_field_name=redirect_field_name
    )
        
    if function:
        return actual_decorator(function)
    return actual_decorator


def all_heads_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user belongs to site,
    redirects to the log-in page if necessary.
    '''
    
    actual_decorator = user_passes_test(
    # lambda u: u.is_active and u.is_student or u.is_superuser,  
    lambda user: user.is_staff or user.is_superuser, #or user.is_head,
    login_url=login_url,
    redirect_field_name=redirect_field_name
    )
        
    if function:
        return actual_decorator(function)
    return actual_decorator


#USIGING THE GROUP REQUIRED DECORATOR NOT THE ABOVE SINGLES

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.only('name').filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='login') #403


def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise Http404

        return wrapper

    return decorator


# check if user is using default password


def default_passeord(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='password_change'):
    '''
    Decorator for views that checks that the logged in user is using the default password,
    redirects to change  password page if necessary.
    '''
    default_password = config('DEFAULT_PASSWORD')
    
    actual_decorator = user_passes_test(
    lambda user: not check_password(default_password,user.password),
    login_url=login_url,
    redirect_field_name=redirect_field_name
    )
        
    if function:
        return actual_decorator(function)
    return actual_decorator

