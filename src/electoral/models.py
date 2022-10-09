from django.db import models
from django.utils import timezone

# Create your models here.

class Position(models.Model):
    '''
    Attributes for all the positions for which the election is
    being held.
    '''
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class Candidate(models.Model):
    '''
    Model which will define the attribute for the candidates
    standing up for the election
    '''
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='candidates')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    '''
    Details and status of students who attended the election voting
    '''
    class VotingStatus(models.TextChoices):
        REGISTERED = 'R', 'Registered'
        OPENED = 'O', 'Opened'
        SUBMITTED = 'S', 'Submitted'
        DECLINED = 'D', 'Declined'

    register_number = models.CharField(max_length=32, unique=True)
    vote_status = models.CharField(max_length=1, choices=VotingStatus.choices, default=VotingStatus.REGISTERED, editable=False)
    last_update = models.DateTimeField(default=timezone.now)
    
    def clean(self):
        self.register_number = self.register_number.upper()

    def __str__(self) -> str:
        return f"{self.register_number}"

class Vote(models.Model):
    '''
    Model which will hold all the vote results
    '''
    position = models.ForeignKey(Position, on_delete=models.CASCADE, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=False)
    voted_by = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.position} - {self.candidate}"

