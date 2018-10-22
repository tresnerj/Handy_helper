from django.shortcuts import render, redirect
from .models import *
from apps.login_reg.models import *
from django.contrib import messages

def index(request):
    if 'id' in request.session:
        context = {
            'user' : Users.objects.get(id = request.session['id']),
            'user_jobs' : Jobs.objects.filter(user_id = request.session['id']), 
            'all_jobs' : Jobs.objects.exclude(user_id = request.session['id']),
            'my_jobs' : JobsAssigned.objects.filter(user_id = request.session['id']),
        }
        return render(request, 'jobs/index.html', context)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def addJob(request):
    if 'id' in request.session:
        return render(request, 'jobs/addjob.html')
    return redirect('/')


def add(request):
    if request.method == 'POST':
        errors = Jobs.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addJob')
        user = Users.objects.get(id = request.session['id'])
        Jobs.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], assigned='no', user=user)
        return redirect('/dashboard')
    return redirect('/addJob')

def view(request, id):
    tf = True
    try:
        already = JobsAssigned.objects.get(orig_id=id)
        if already:
            tf = False
    except:
        pass
    context = {
        'job' : Jobs.objects.get(id = id),
        'tf' : tf,
    }
    return render(request, 'jobs/view.html', context)

def edit(request, id):
    job = Jobs.objects.get(id = id)
    if job.user_id == request.session['id']:
        context = {
            'job' : job,
        }
        return render(request, 'jobs/edit.html', context)
    return redirect('/')

def processEdit(request, id):
    if request.method == 'POST':
        errors = Jobs.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{id}')
        job = Jobs.objects.get(id = id)
        job.title = request.POST['title']
        job.desc = request.POST['desc']
        job.location = request.POST['location']
        job.save()
    return redirect('/dashboard')

def getJob(request, id):
    job = JobsAssigned.objects.filter(orig_id = id)
    if not job:
        job = Jobs.objects.get(id = id)
        user = Users.objects.get(id=request.session['id'])
        getjob = JobsAssigned.objects.create(title=job.title, desc=job.desc, location=job.location, user=user, orig_id=job.id, created_at=job.created_at)
        job.assigned = 'yes'
        job.save()
    return redirect('/dashboard')


def delete(request, id):
    job = Jobs.objects.get(id = id)
    if job.user_id == request.session['id']:
        job = Jobs.objects.get(id = id)
        job.delete()
    return redirect('/dashboard')

def done(request, id):
    job = JobsAssigned.objects.get(id = id)
    if job.user_id == request.session['id']:
        deletejob = Jobs.objects.get(id = job.orig_id)
        deletejob.delete()
        job.delete()
    return redirect('/dashboard')




