from django.shortcuts import render
from electoral.models import Candidate, Position, Student, Vote
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required


import logging
log = logging.getLogger(__name__)

def voting_page(request):
    '''
    Render the voting page with details of all active candidates
    grouped by their competing positions
    '''
    try:
        register_number = request.session['registerno']
        s = Student.objects.get(register_number=register_number)
        s.vote_status = Student.VotingStatus.OPENED
        s.save()
    except Student.DoesNotExist:
        del request.session['registerno']
        return HttpResponseRedirect(reverse('home'))
    except KeyError:
        return HttpResponseRedirect(reverse('home'))

    all_candidates = Candidate.objects.filter(active=True).order_by('position__order')
    
    # Dict structure for all candidates, grouped by their position
    positions_d = {}
    for candidate in all_candidates:
        position = candidate.position.name
        try:
            positions_d[position].append(candidate)
        except KeyError:
            positions_d[position] = [candidate]

    if request.method == 'POST':
        flag = request.POST.get('submit_vote')
        if flag:
            save_vote(request, positions_d)
            s.vote_status = Student.VotingStatus.SUBMITTED
            s.save()
        else:
            decline_vote(request)
            s.vote_status = Student.VotingStatus.DECLINED
            s.save()
        return HttpResponseRedirect('/')

    # elif request.method == 'GET':
    return render(request, 'electoral/voting.html', context={
        'positions': positions_d,
        'registerno': register_number,
        'is_track_enabled': settings.TRACK_STUDENT_VOTES,
        'allow_cancel_vote': settings.ALLOW_CANCEL_VOTE,
    })

def save_vote(request, positions_d):
    # Get student register number from the session
    register_number = request.session['registerno']

    for idx, position in enumerate(positions_d.keys()):
        candidate_id = request.POST[f'nav-input-id-{idx}']
        v = Vote(
            position = Position.objects.get(name=position),
            candidate = Candidate.objects.get(id=candidate_id)
        )

        if settings.TRACK_STUDENT_VOTES:
            # WARN: This will start tracking who casted the vote
            # PRIVACY CONCERNS SHOULD BE HIGHLIGHTED ON VOTING PAGE
            try:
                student = Student.objects.get(register_number=register_number)
                v.voted_by = student
            except Student.DoesNotExist:
                log.warn(f'Student with register number {register_number} not found in DB')
        v.save()
    del request.session['registerno']

def decline_vote(request):
    # TODO: Mark an entry in DB
    del request.session['registerno']

@login_required
def results(request):
    pass
