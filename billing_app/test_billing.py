import requests


#check Health endpoint
def test_get_Check_Health_status_code_expected_200():

     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/billing-api/health'
     response = requests.get(url,)
     assert response.status_code == 200





#Test Post provider endpoint success is code 201 
def test_post_provider_with_name_Testprovider1_status_code_expected_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/provider'
     myobj = {"name": "Testprovider1"}
     response = requests.post(url, json = myobj)
     assert response.status_code == 201


def test_put__provider_with_id_1002_status_code_expected_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/provider/1002'
     myobj = {"name": "Testprovider1002"}
     response = requests.put(url, json = myobj)
     assert response.status_code == 201


#get specific provider with the id
def test_get__specific_provider_with_id_1002_status_code_expected_200():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/provider/1002'
     response = requests.get(url)
     assert response.status_code == 200


#Test Post rates endpoint success is code 201 
def test_post__weight_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/weight'
     myobj = {"container": "","weight": "","truck_id": "","unit": "","force": ""}
     response = requests.post(url, json = myobj)
     assert response.status_code == 201

#Post Rates loads the rates excel file in mounted volume IN
# def test_post__rates_201():

#      url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/rates'
#      response = requests.post(url,)
#      assert response.status_code == 201


#downloads rates data into excel
def test_get__rates_200():

     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/rates'
     response = requests.get(url,)
     assert response.status_code == 200



#get billing 


#Test Post truck endpoint success is code 201 
def test_post__truck_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8082/truck'
     myobj = {"id": "111-11-111","provider_id": 1002 }
     response = requests.post(url, json = myobj)
     assert response.status_code == 201
























































# def test_get_locations_for_us_90210_check_content_type_equals_json():
#      response = requests.get("http://api.zippopotam.us/us/90210")
#      assert response.headers["Content-Type"] == "application/json"

# def test_get_locations_for_us_90210_check_country_equals_united_states():
#      response = requests.get("http://api.zippopotam.us/us/90210")
#      response_body = response.json()
#      assert response_body["country"] == "United States"

# def test_get_locations_for_us_90210_check_city_equals_beverly_hills():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert response_body["places"][0]["place name"] == "Beverly Hills"
