from __future__ import absolute_import, unicode_literals

from celery import shared_task

from api.models import Submission
from api import submission_service


@shared_task
def update_submissions():
    submissions = Submission.objects.filter(status=Submission.StatusEnum.EVALUATION)

    for submission in submissions:
        if not submission.internal_id:
            internal_id, status = submission_service.post_submission(submission.function_code)
            submission.internal_id = internal_id
            submission.status = status
        else:
            internal_id, status = submission_service.get_submission(submission.internal_id)
            submission.status = status

        submission.save()
