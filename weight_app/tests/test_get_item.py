import requests
base_url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8081'


def test_item_withId():     
    response=requests.get(f'{base_url}/item/t0001')
    assert response.status_code==200

def test_item_withoutId():   
    response=requests.get(f'{base_url}/item')
    assert response.status_code==404