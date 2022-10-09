from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from electoral.models import Student
from django.db import IntegrityError

def index(request):
    if request.method == 'POST':
        register_number:str = request.POST['registerno']
        register_number = register_number.upper()
        try:
            has_voted = create_student(register_number)
            if has_voted == True:
                return render(request, 'home/index.html', {
                    'message': f'{register_number} already completed voting!'
                })
        except IntegrityError as e:
            return render(request, 'home/index.html', {
                'message': e
            })
        request.session['registerno'] = register_number
        return HttpResponseRedirect(reverse('voting'))
    
    try:
        register_number = request.session['registerno']
        # If register number is set, proceed to voting page
        return HttpResponseRedirect(reverse('voting'))
    except KeyError:
        pass
    return render(request, 'home/index.html')

def create_student(register_number):
    s, created = Student.objects.get_or_create(register_number = register_number)
    if s.vote_status == Student.VotingStatus.SUBMITTED or s.vote_status == Student.VotingStatus.DECLINED:
        return True
    else:
        return False
