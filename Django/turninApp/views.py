from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
import subprocess 
import json
import os.path

sudotoken = "b81ea16b6bcefcdd4e24269a79971e2585b67617"

def signin(request):
    
    command = 'curl -u forCSEE:' + sudotoken + ' https://api.github.com/user/repository_invitations'
    command = command.split()
    s = subprocess.check_output(command) 
    s = s.decode('utf-8')
    s = json.loads(s)

    for i in s:
      print(i['id'])
      print(i['repository']['html_url'])

      col_id = str(i['id'])
      col_name = i['repository']['full_name']
      col_repo = i['repository']['name']
      user_id = i['repository']['owner']['login']


      command = 'curl --request PATCH -i -u forCSEE:' + sudotoken + ' https://api.github.com/user/repository_invitations/' + col_id
      command = command.split()
      subprocess.check_output(command)
      
      command = 'git clone https://forCSEE:' + sudotoken + '@github.com/' + col_name +'.git'
      command = command.split()
      subprocess.check_output(command)
     
      f = open(col_repo+'/.turnincode', 'r')
      line = f.readline()
      line = line.rstrip('\n')
            
      if Student.objects.filter(student_id=user_id).exists():
          print("student")
          if Homework.objects.filter(hw_base=line).exists():
              h = Homework.objects.get(hw_base=line)
              hs = Homework_Student(hw=h, std=user_id)
              hs.save()
      elif Professor.objects.filter(professor_id=user_id).exists():
          eval_repo = i['repository']['html_url'] + '.git'
          h = Homework(hw_base=line, hw_eval=eval_repo, hw_madeby=user_id)
          h.save()
          print("professor")
      f.close()
      # .turnincode 유무 판단 
      # 있으면, basecode url 이랑hw 모델의 base_url 과 같은것을 찾아서 학생과의 relationship을 구축 ! 
      # 없으면, 교수라고 판단하고 아무것도 하지 않음. 

    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def success_login(request):
    current_user=request.user
    print(current_user)
    if current_user == "admin":
        return HttpResponse("you are logged in as admin. please check it")
    elif Student.objects.filter(student_id = current_user).exists():
        return redirect('student-page')
    elif Professor.objects.filter(professor_id = current_user).exists():
        return redirect('professor-page')
    else:
        print("not registered user")
        return redirect('signup')

def student_page(request):
    return render(request, 'student_page.html')

def student_mypage(request):
    current_user = request.user
    if Homework_Student.objects.filter(std = current_user).exists():
        hs = Homework_Student.objects.filter(std=current_user)
        hwlist = []
        for h in hs:
            hinfo = [h.hw.id, h.hw.hw_name]
            hwlist.append(hinfo)
        hwlist = list(set(map(tuple, hwlist)))
        return JsonResponse(hwlist, safe=False)
    return HttpResponse()

def professor_page(request):
    current_user = request.user
    p = Professor.objects.get(professor_id=current_user)
    if p.professor_status == True:
        return render(request, 'professor_page.html')
    else:
        return HttpResponse("You don't have any permission to access professor page. Please wait for authentication")

def current_user(request):
    current_user = request.user
    return JsonResponse(str(current_user), safe=False)

def runcode(request, hw_id):
    current_user = request.user
    h = Homework.objects.get(id=hw_id)
    hs = Homework_Student.objects.filter(std=current_user, hw=h)

    current_score = hs.last().score
    return JsonResponse(str(current_score), safe=False)

def getscore(request, hw_name):
    hwlist = Homework_Student.objects.all()
    scorelist = []
    for i in hwlist:
        if i.hw.hw_name == hw_name:
            score = Homework_Student.objects.filter(std=i.std).last().score 
            slist = [i.std , score] 
            scorelist.append(slist)
        scorelist = list(set(map(tuple, scorelist)))   
    return JsonResponse(scorelist, safe=False)

def getscdetail(request, hw_name, std_id):
    hwlist = Homework_Student.objects.filter(std=std_id)
    stdinfo = Student.objects.get(student_id = std_id)
    scoredetail = [stdinfo.student_name, stdinfo.student_number]
    for i in hwlist:
        if i.hw.hw_name == hw_name:
            slist = [i.score]
            scoredetail.append(slist)
            
    return JsonResponse(scoredetail, safe=False)

'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
#    authentication_classes = (TokenAuthentication, )
#    permission_classes = (IsAuthenticated, )
'''
def updatehw(request, hw_id):
    h = Homework.objects.get(id=hw_id)
    hw = [h.hw_base, h.hw_eval, h.hw_madeby]
    return JsonResponse(hw, safe=False)
    
def student_getinfo(request, hw_id):
    h = Homework.objects.get(id=hw_id)
    hs = Homework_Student.objects.filter(hw=h, std=request.user)
    hslist = [h.hw_name, h.hw_base, h.hw_description, h.hw_duedate]
    hw = []
    for i in hs:
        hw.append(i.score)
    hslist.append(hw)    

    return JsonResponse(hslist, safe=False)


def gethw(request):
    user = request.user
    print(user)
    hs = Homework.objects.filter(hw_madeby=user)
    if hs.exists():
        hwlist = []
        for h in hs:
            hw = [ h.id, h.hw_name, h.hw_base, h.hw_eval, h.hw_description, h.hw_duedate ]
            hwlist.append(hw)
        return JsonResponse(hwlist, safe=False)
    else:
        print("not exist")
    return HttpResponse()

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

@csrf_exempt
def webhook(request):
    result="before grading"
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        print(payload)
        result=payload
    return HttpResponse(result)

