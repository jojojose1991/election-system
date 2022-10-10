from django.contrib import admin
from electoral.models import Position, Candidate, Student, Vote

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    # pass

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'total_votes', 'active')

    def total_votes(self, obj):
        return Vote.objects.filter(candidate=obj).count()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'register_number', 'vote_status', 'last_update')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'candidate', 'voted_by')
    list_editable = ()
