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
            match = re.match("(\d{3})$", area_code)
            assert match is not None
            self.assertEquals(len(match.groups()), 1) # ensures 3 digits

    # regex check using a regex equation from https://www.safaribooksonline.com/library/view/regular-expressions-cookbook/9781449327453/ch04s02.html
    def test_has_full_number(self):
        response = app.get_results(1)
        fetched = json.loads(response)
        phone_number = fetched[0].get("phone_number")
        match = re.match("\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$",phone_number)
        assert match is not None

    # regex pattern should also work for phone numbers of ten digits, however it's not currently functional for +1 phone numbers so it currently assumes local country area codes
    def test_all_full_numbers(self):
        response = app.get_results()
        fetched = json.loads(response)
        for f in fetched:
            phone_number = f.get("phone_number")
            match = re.match("\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$",phone_number)
            assert match is not None
            self.assertEquals(len(match.groups()),3)

    # check that number of comments is a number
    def test_number_of_comments(self):
        response = app.get_results(1)
        fetched = json.loads(response)
        report_count = fetched[0].get("report_count")
        match = re.match("([\d])+$",report_count)
        assert match is not None

    # check that all numbers of comments are numbers
    def test_all_number_of_comments(self):
        response = app.get_results()
        fetched = json.loads(response)
        for f in fetched:
            report_count = f.get("report_count")
            match = re.match("([\d])+$",report_count)
            assert match is not None
            print report_count

    


if __name__ == "__main__":
    unittest.main()