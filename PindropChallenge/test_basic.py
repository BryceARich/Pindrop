import os
import unittest
import requests

import data
import app


class BasicTests(unittest.TestCase):

    # Tests for the vaious desired endpoints
    def test_request(self):
        response = requests.get("http://localhost:5000/interview/api/v1.0/results")
        self.assertEquals(response.status_code, 200)

    def test_request2(self):
        response = requests.get("http://localhost:5000/interview/api/v1.0/results/1")
        self.assertEquals(response.status_code, 200)

    def test_areaRequest(self):
        response = requests.get("http://localhost:5000/interview/api/v1.0/resultsForArea/770")
        self.assertEquals(response.status_code, 200)

    def test_areaRequest2(self):
        response = requests.get("http://localhost:5000/interview/api/v1.0/resultsForArea/770/2")
        self.assertEquals(response.status_code, 200)

    def test_incorrectEndpoint(self):
        response = requests.get("http://localhost:5000/interview/api/v1.0/nonexistent")
        self.assertEquals(response.status_code, 404)

    # def test_get_results(self):
        # result = app.get

if __name__ == "__main__":
    unittest.main()