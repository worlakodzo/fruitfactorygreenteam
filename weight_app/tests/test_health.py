import requests
base_url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8081'

def test_health_of_system():     
    response=requests.get(f'{base_url}/weight-api/health')
    assert response.status_code==200

