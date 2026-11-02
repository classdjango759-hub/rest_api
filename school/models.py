from django.db import models

class School(models.Model):
    name = models.CharField()
    avg_student_per_year = models.FloatField()
    is_accredited = models.BooleanField()
    established_since = models.IntegerField()

    def __str__(self):
        return f"{self.name} established since {self.established_since}"
    