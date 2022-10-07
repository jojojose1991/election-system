from django.db import models

# Create your models here.

class Position(models.Model):
    '''
    Attributes for all the positions for which the election is
    being held.
    '''
    name = models.CharField(max_length=100)

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

    def __str__(self):
        return f"{self.name}"