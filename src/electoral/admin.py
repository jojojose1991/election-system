from django.contrib import admin
from electoral.models import Position, Candidate

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass
