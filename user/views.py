# Create your views here.
from datetime import date
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib import messages

from user.forms import UserForm,ResetPasswordForm
from django.urls import reverse
from user.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class CreateUser(View):
    template_name = 'user/create.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],  # Using email as username
                is_active=True,
            )
            # Optional extra fields if your User model supports them
            if hasattr(user, 'mobile'):
                user.mobile = form.cleaned_data.get('mobile')
            if hasattr(user, 'country_code'):
                user.country_code = form.cleaned_data.get('country_code')
            if hasattr(user, 'role'):
                user.role = form.cleaned_data.get('role')
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Add groups (permissions)
            for group in form.cleaned_data['groups']:
                user.groups.add(group)

            # AJAX support
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/otp-verify/'})

            messages.success(request, "Successfully Registered")
            return redirect('login')

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(form.errors, status=400)

            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'form': form})
            

class UserList(View):

    template_name = "base/dashboard.html"

    # def dispatch(self, request, *args, **kwargs):
    #     # if request.user.role != "SUPER_ADMIN":
    #     #     messages.warning(self.request, 'You Have Not Permission TO access this project')
    #     #     return redirect('base:dashboard')

    #     return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        users = User.objects.active()

        results_per_page = 10
        page = request.GET.get('page', 1)
        paginator = Paginator(users, results_per_page)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context = {
            "users":users,
            "data" : [page,results_per_page],
        }
        return render(request,self.template_name, context)
            
        
class EditUser(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "SUPER_ADMIN":
            messages.warning(self.request, 'You Have Not Permission TO access this project')
            return redirect('base:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self,request,id):

        user = User.objects.get(id=id)
        form = UserForm(edit=True,user=user)

        context = {
            'form': form,
            'edit_user':user
        }
        return render(request,'users/edit.html',context)

    def post(self,request,id):
        user = User.objects.get(id=id)
        form = UserForm(request.POST, edit=True , user=user)

        if form.is_valid():
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.name = user.first_name + " " + user.last_name
            user.mobile = form.cleaned_data['mobile']
            user.country_code=form.cleaned_data['country_code']
            user.role=form.cleaned_data['role']
            user.email=form.cleaned_data['email']
            user.username = form.cleaned_data['email']
            user.save()
            
            user.groups.clear()  # Clear existing groups
            for group in form.cleaned_data['groups']:
                user.groups.add(group)

            messages.success(
                    self.request, "Successfully Updated")
            return redirect('users:users-list')
    
        else:
            messages.error(self.request ,form.errors)
            return redirect('users:edit-users',id=id)


class ResetPasswordView(View):
    template_name = 'users/resetpassword.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "SUPER_ADMIN":
            messages.warning(self.request, 'You Have Not Permission TO access this project')
            return redirect('base:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        user=User.objects.get(id=id)
        form = ResetPasswordForm()
        context = {
            'form': form,
            'edit_user':user
        }
        return render(request, self.template_name , context)

    def post(self, request, id):
        user=User.objects.get(id=id)
        form = ResetPasswordForm(request.POST)

        context = {
            'form': form,
            'user':user
        }
        
        if form.is_valid():

            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
   
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password Successfully Updated")
                return redirect('users:users-list')
            
            else:
                messages.error(request, "Passwords do not match")
                return redirect(reverse('users:reset_password', args=[id]))


        return render(request, self.template_name , context)
    

    
    

