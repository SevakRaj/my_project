from django.urls import path,include
from django.contrib.auth.decorators import login_required
# from user.views import CreateUser,UserList,EditUser,ResetPasswordView,Dashboard, CreateTask, AllUserTaskList, LogedUserList
app_name = "users"

urlpatterns = [
    # path("create/",login_required(CreateUser.as_view()), name="create-user"),
    # path("list/",login_required(UserList.as_view()), name="users-list"),
    # path("tasked-user-list/",login_required(LogedUserList.as_view()), name="users-list-task"),
    # path("<slug:id>/edit",login_required(EditUser.as_view()), name="edit-users"),

    # path('<slug:id>/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    # path("dashboard/", login_required(Dashboard.as_view()), name="users-dashboard"),
    # path("daily-task/", login_required(CreateTask.as_view()), name="user-create-task"),
    # path("all-users-task-list/", login_required(AllUserTaskList.as_view()), name="all-users-task-list"),
    # path("<slug:slug>/task-list", login_required(AllUserTaskList.as_view()), name="user-task-list"),
    
    # path('api/',include('users.api_urls',namespace='users_api')),

]