import unittest
import requests


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    UNKNOWN_URL="{}/unknown".format(API_URL)
    WEIGHT_URL = "{}/weight".format(API_URL)

    WEIGHT_OBJ = {
    "direction": "IN",
    "license": "L-28738",
    "unit": "lbs",
    "force": False,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 124
}

    def test_unknown(self):
        r = requests.get(ApiTest.UNKNOWN_URL)
        self.assertEqual(r.status_code, 200) 
        self.assertTrue(r.json)      

    # Post requires json file format POST /weight
    def test_weight_post(self):
        r = requests.post(ApiTest.WEIGHT_URL, json=ApiTest.WEIGHT_OBJ)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["bruto"], 124)

# {
#     "bruto": 129,
#     "id": 7,
#     "truck": "AT-c0938"
# }
        