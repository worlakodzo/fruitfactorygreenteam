import unittest
import requests


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    UNKNOWN_URL="{}/unknown".format(API_URL)
    WEIGHT_URL = "{}/weight".format(API_URL)

    WEIGHT_OBJ_IN_FORCE = {
    "direction": "in",
    "truck": "L-387380",
    "force": True,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}

    WEIGHT_OBJ_IN_NOT_FORCE = {
    "direction": "in",
    "truck": "L-387380",
    "force": False,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}


    WEIGHT_OBJ_OUT_FORCE = {
    "direction": "out",
    "truck": "L-387380",
    "force": True,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}

    WEIGHT_OBJ_OUT_NOT_FORCE = {
    "direction": "out",
    "truck": "L-387380",
    "force": False,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}

    WEIGHT_OBJ_NONE_FORCE = {
    "direction": "none",
    "truck": "L-387380",
    "force": True,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}

    WEIGHT_OBJ_NONE_NOT_FORCE = {
    "direction": "none",
    "truck": "L-387380",
    "force": False,
    "produce": "mangoes",
    "containers": "T-17077, T-13972, T-17267",
    "weight": 120
}




    def test_unknown(self):
        r = requests.get(ApiTest.UNKNOWN_URL)
        self.assertEqual(r.status_code, 200) 
        self.assertTrue(r.json)      

    # Post requires json file format POST /weight
    def test_weight_post_one(self):
        r = requests.post(ApiTest.WEIGHT_URL, json=ApiTest.WEIGHT_OBJ_IN_FORCE)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 3)



    def test_weight_post(self):
        # Sending same payload twice without forcing overriding existing info
        requests.post(ApiTest.WEIGHT_URL, json=ApiTest.WEIGHT_OBJ_OUT_FORCE)
        r = requests.post(ApiTest.WEIGHT_URL, json=ApiTest.WEIGHT_OBJ_IN_FORCE)
        self.assertEqual(r.status_code, 200)