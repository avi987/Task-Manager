from django.http import HttpResponse,Http404
from .models import Task , Team , Comments, User
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.edit import CreateView,UpdateView,View
from .forms import UserForm
from django.contrib.auth import authenticate , login
from django.db.models import Q
from django import forms
from django.forms import ModelMultipleChoiceField
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        teams = Team.objects.filter(users=request.user)
        searchdata = request.GET.get("srch")
        if searchdata:
            tasks = []
            for team in teams:
                tasks += team.task_set.filter(Q(task_title=searchdata))
            teams = teams.filter(Q(team_name=searchdata))
            return HttpResponse(render(request,'tasks/index.html',{'teams':teams,'tasks':tasks,}))
        else:
            return HttpResponse(render(request,'tasks/index.html',{'teams':teams,}))
    else:
        return redirect('tasks:login')

def team_details(request,team_id):
    if request.user.is_authenticated:
        team = get_object_or_404(Team,pk=team_id,users=request.user)
        return HttpResponse(render(request,'tasks/team_details.html',{'team':team,}))
    else:
        return redirect('tasks:login')

def team_members(request,team_id):
    if request.user.is_authenticated:
        team = get_object_or_404(Team,pk=team_id,users=request.user)
        members = team.users.all
        return HttpResponse(render(request,'tasks/team_members.html',{'team':team,'members':members}))
    else:
        return redirect('tasks:login')

def task_details(request,team_id,task_id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task,pk=task_id)
        if request.user in task.task_team.users.all():
            comments = Comments.objects.filter(task=task)
            return HttpResponse(render(request,'tasks/task_details.html',{'task':task,'comments':comments}))
        else:
            raise Http404
    else:
        return redirect('tasks:login')

def allTasks(request):
    if request.user.is_authenticated:
        teams = Team.objects.filter(users=request.user)
        tasks = []
        for team in teams:
            tasks += Task.objects.filter(task_team=team)
        return HttpResponse(render(request,'tasks/alltasks.html',{'tasks':tasks}))
    else:
        return redirect('tasks:login')

def tasksCreatedByUser(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(createdBy=request.user)
        return HttpResponse(render(request,'tasks/userCreatedTasks.html',{'tasks':tasks}))
    else:
        return redirect('tasks:login')

class TeamCreate(LoginRequiredMixin,CreateView):
    model = Team
    fields = ['team_name','users']
    login_url = 'tasks:login'

    def get_form(self, form_class=None):
        form = super(TeamCreate, self).get_form(form_class)
        qset = User.objects.all()
        form.fields['users'] = ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=qset)
        return form


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['task_title','task_description','task_assignee','task_status']
    login_url = 'tasks:login'

    def dispatch(self, request, *args, **kwargs):
        self.task_team = get_object_or_404(Team, pk=kwargs['team_id'], users=request.user)
        self.createdBy = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(TaskCreate, self).get_form(form_class)
        qset = self.task_team.users.all()
        form.fields['task_assignee'] = ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=qset)
        return form

    def form_valid(self, form):
        form.instance.task_team = self.task_team
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['task_title','task_description','task_assignee','task_status']
    login_url = 'tasks:login'

    def dispatch(self, request, *args, **kwargs):
        self.task_team = get_object_or_404(Team, pk=kwargs['team_id'], users=request.user)
        self.pk = kwargs['pk']
        if request.user in self.task_team.users.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def get_form(self, form_class=None):
        form = super(TaskUpdate, self).get_form(form_class)
        qset = self.task_team.users.all()
        form.fields['task_assignee'] = ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=qset)
        return form

    def get_success_url(self,*args,**kwargs):
        return reverse_lazy('tasks:task_details',kwargs={'team_id':self.task_team.id,'task_id':self.pk})


def taskDelete(request,team_id,task_id):
    if request.user.is_authenticated:
        task = get_object_or_404(Task,pk=task_id)
        print(task.createdBy,request.user)
        if task.createdBy == request.user:
            task.delete()
            team = get_object_or_404(Team,pk=team_id,users=request.user)
            return HttpResponse(render(request,'tasks/team_details.html',{'team':team}))
        else:
            raise Http404
    else:
        return redirect('tasks:login')
class UserFormView(View):
    form_class = UserForm
    template_name = 'tasks/register.html'

    def get(self , request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('tasks:index')

        return render(request,self.template_name,{'form':form})

class Comment(LoginRequiredMixin,CreateView):
    model = Comments
    fields = ['comment']
    login_url = 'tasks:login'

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs['task_id'])
        if self.task.task_team.users is request.user:
            self.commentedBy = request.user
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        form.instance.task = self.task
        form.instance.commentedBy = self.request.user
        return super().form_valid(form)