import os
import re
import unittest
import requests

import data
import app
import json


class BasicTests(unittest.TestCase):

    def is_json(self, input):
        try:
            json.obj = json.loads(input)
        except ValueError, e:
            return False
        return True

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

    # Tests for if the results are in json valid format
    def test_get_results_json(self):
        self.assertTrue(self.is_json(app.get_results()))

    def test_get_results_by_area_json(self):
        self.assertTrue(self.is_json(app.get_results_by_area(770)))

    def test_has_area_code(self):
        response = app.get_results(1)
        fetched = json.loads(response)
        area_code = fetched[0].get("area_code")
        self.assertEqual(len(area_code), 3) # ensures 3 characters
        match = re.match("(\d{3})", area_code)
        self.assertEquals(len(match.groups()), 1) # ensures 3 digits

    # discovered original code had some "area_code"s that were not entirely digits
    def test_all_area_codes(self):
        response = app.get_results()
        fetched = json.loads(response)
        for f in fetched:
            area_code = f.get("area_code")
            self.assertEqual(len(area_code),3)
            match = re.match("(\d{3})", area_code)
            print area_code
            assert match is not None
            self.assertEquals(len(match.groups()), 1) # ensures 3 digits


if __name__ == "__main__":
    unittest.main()