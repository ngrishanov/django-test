import uuid

from django.db import models


class Submission(models.Model):
    class StatusEnum(models.TextChoices):
        EVALUATION = 'evaluation'
        CORRECT = 'correct'
        WRONG = 'wrong'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    internal_id = models.IntegerField(unique=True, null=True, blank=True)
    function_code = models.TextField()
    status = models.TextField(choices=StatusEnum.choices, default=StatusEnum.EVALUATION)
