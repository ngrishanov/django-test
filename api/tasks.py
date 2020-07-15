from __future__ import absolute_import, unicode_literals

from celery import shared_task

from api.models import Submission
from api import submission_service


@shared_task
def update_submission(submission_uuid):
    submission = Submission.objects.get(pk=submission_uuid)

    if not submission.internal_id:
        internal_id, status = submission_service.post_submission(submission.function_code)
        submission.internal_id = internal_id
    else:
        internal_id, status = submission_service.get_submission(submission.internal_id)

    submission.status = status
    submission.save()


@shared_task
def add_update_submission_tasks():
    submissions = Submission.objects.filter(status=Submission.StatusEnum.EVALUATION)

    for submission in submissions:
        update_submission.delay(submission.uuid)
