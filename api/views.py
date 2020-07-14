import json

from django.http import JsonResponse
from django.views import View

from api.models import Submission


class SubmissionView(View):
    def get(self, request, submission_uuid):
        try:
            submission = Submission.objects.get(pk=submission_uuid)
        except Submission.DoesNotExist:
            return JsonResponse({'error': 'Submission not found'}, status=404)

        return JsonResponse({'error': None, 'result': {'status': submission.status}})


class SubmissionsView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request JSON'}, status=400)

        function_code = data.get('function_code')

        if not function_code:
            return JsonResponse({'error': 'function_code is required'}, status=400)

        submission = Submission(function_code=function_code)
        submission.save()

        return JsonResponse({'error': None, 'result': {'uuid': submission.uuid, 'status': submission.status}})
