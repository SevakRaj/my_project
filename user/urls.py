from django.urls import path,include
from django.contrib.auth.decorators import login_required
from user.views import CreateUser,UserList,ResetPasswordView
app_name = "user"

urlpatterns = [
    path("create/",(CreateUser.as_view()), name="create"),
    path("list/",login_required(UserList.as_view()), name="list"),
    # path("tasked-user-list/",login_required(LogedUserList.as_view()), name="users-list-task"),
    # path("<slug:id>/edit",login_required(EditUser.as_view()), name="edit-users"),

    path('<slug:id>/reset-password/', ResetPasswordView.as_view(), name='reset_password'),

]