import requests


#check Health endpoint
def test_get_Check_Health_status_code_expected_200():

     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8085/billing-api/health'
     response = requests.get(url,)
     assert response.status_code == 200





#Test Post provider endpoint success is code 201 
def test_post_provider_with_name_Testprovider1_status_code_expected_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8085/provider'
     myobj = {"name": "Testprovider1"}
     response = requests.post(url, json = myobj)
     assert response.status_code == 201



#get specific provider with the id
def test_get__specific_provider_with_id_1002_status_code_expected_200():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8085/provider/1002'
     response = requests.get(url)
     assert response.status_code == 200


#Test Post rates endpoint success is code 201 
def test_post__weight_201():
     
     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8085/weight'
     myobj = {"container": "","weight": "","truck_id": "","unit": "","force": ""}
     response = requests.post(url, json = myobj)
     assert response.status_code == 201



#downloads rates data into excel
def test_get__rates_200():

     url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8085/rates'
     response = requests.get(url,)
     assert response.status_code == 200





















































