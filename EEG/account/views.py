from django import forms
from django.contrib.auth.models import User
from EEG.data_store.models import Owner, Viewer
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def confirm_registration(request, username, token):
    """
     :Args:
          | username: username when the user put in the registration
          | token: unique token for each user for the registration


     :Returns:
          | the user state is active in the database
    """
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})


class RegistrationForm(forms.Form):
    """
     :Args:
          | form: the user need to provide the information for the registration. As username, email, password



     :Returns:
          | the form provided by user
    """
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm password',
                                widget=forms.PasswordInput())
    student = forms.BooleanField(required=False, widget=forms.HiddenInput())
    professor = forms.BooleanField(required=False, widget=forms.HiddenInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email).exclude(username__startswith='INTERN'):
            raise forms.ValidationError("This email is already being used")
        return email

def register(request):
    """
     :Args:
          | request: request from the website


     :Returns:
          | the information in the registration form and give user a link to active the account
    """

    context = {}
    if request.method == 'GET':
        prefill = {}
        if request.GET.get('student'):
            prefill = {'student': True}
        context['form'] = RegistrationForm(prefill)
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)

    former_user = User.objects.filter(email=form.cleaned_data['email'])

    if len(former_user) == 1:
        new_user = former_user[0]
        new_user.username = form.cleaned_data['username']
    else:
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'])
    new_user.set_password(form.cleaned_data['password1'])

    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()

    # generate professor or student account
    if form.cleaned_data['professor']:
        Owner.objects.create(user=new_user)
    if form.cleaned_data['student']:
        if not hasattr(new_user, 'viewer'):
            Viewer.objects.create(user=new_user)

    #new_user.profile.save()
    #new_user.network.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to SynMetric.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(),
       reverse('confirm', args=(new_user.username, token)))

    mail.send_mail(subject="Verify your email address",
                   message=email_body,
                   from_email="synmetric.cmu@gmail.com",
                   recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'needs-confirmation.html', context)


def change_password(request):
    """
     :Args:the request from the website



     :Returns:
          | the new password reset by the user
    """
    if request.method == 'GET':
        form = ChangepwdForm()
        return render_to_response('change_password.html', RequestContext(request, {'form': form}))
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return redirect('/EEG/')
                #return render_to_response('loginin/change_password.html', RequestContext(request, {'changepwd_success':True}))
            else:
                return render_to_response('change_password.html', RequestContext(request, {'form': form, 'oldpassword_is_wrong': True}))
        else:
            return render_to_response('change_password.html', RequestContext(request, {'form': form}))


class FirstLoginForm(forms.Form):
    """
     :Args:forms that provided by the user


     :Returns:
          | the user status is student or professor
    """
    marketer = forms.BooleanField(required=False)
    professor = forms.BooleanField(required=False)
    student = forms.BooleanField(required=False)


@login_required
def first_login(request):
    """
    :Args:the request from the website
    :Returns:
    | since this the first time the user login, we lack of any information for the user in the database. to prevent any confusing situation, we double check the users' situation and return the correct page for them
    """
    if request.method == "GET":
        form = FirstLoginForm()
        if hasattr(request.user, 'owner'):
            if request.user.owner.marketer:
                return redirect('/EEG/market/home')
            return redirect('/EEG/profhome')
        elif hasattr(request.user, 'viewer'):
            return redirect('/EEG/student/home')
        return render_to_response('first_login.html', RequestContext(request, {'form': form}))
    elif request.method == "POST":
        form = FirstLoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['marketer'] and not hasattr(request.user, 'owner'):
                Owner.objects.create(user=request.user, marketer=True)
                return redirect('/EEG/marketer/home')
            elif form.cleaned_data['professor'] and not hasattr(request.user, 'owner'):
                Owner.objects.create(user=request.user, marketer=False)
                return redirect('/EEG/profhome')
            elif form.cleaned_data['student'] and not hasattr(request.user, 'viewer'):
                Viewer.objects.create(user=request.user)
                return redirect('/EEG/student/home')
            else:
                return redirect('/EEG/home')
        else:
            return render_to_response('first_login.html', RequestContext(request, {'form': form}))
