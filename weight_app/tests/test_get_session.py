import requests
base_url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8086'



def test_session():  
    response=requests.get(f'{base_url}/session/10001')
    assert response.status_code==200

def test_session_withoutId():    
    response=requests.get(f'{base_url}/session')
    assert response.status_code==404