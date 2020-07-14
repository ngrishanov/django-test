import json

from django.test import TestCase

from api.models import Submission

# Create your tests here.


class GetSubmissionTest(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(function_code='123')

    def test_submission_doesnt_exist(self):
        response = self.client.get('/api/submissions/00000000-0000-0000-0000-000000000000/')

        body = json.loads(response.content)

        self.assertEqual(404, response.status_code)
        self.assertEqual('Submission not found', body['error'])

    def test_submission_exists(self):
        response = self.client.get(f'/api/submissions/{self.submission.uuid}/')

        body = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(None, body['error'])
        self.assertEqual(self.submission.status, body['result']['status'])


class CreateSubmissionTest(TestCase):
    def test_invalid_json(self):
        response = self.client.post(
            '/api/submissions/',
            'invalid json',
            content_type='application/json',
        )

        body = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid request JSON', body['error'])

    def test_no_function_code(self):
        response = self.client.post(
            '/api/submissions/',
            json.dumps({}),
            content_type='application/json',
        )

        body = json.loads(response.content)

        self.assertEqual(400, response.status_code)
        self.assertEqual('function_code is required', body['error'])

    def test_valid(self):
        response = self.client.post(
            '/api/submissions/',
            json.dumps({'function_code': '123'}),
            content_type='application/json',
        )

        body = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(None, body['error'])
        self.assertIsNotNone(body['result']['status'])
        self.assertIsNotNone(body['result']['uuid'])
