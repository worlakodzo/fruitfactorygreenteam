from app import app

def test_health_of_system():
    web=app.test_client()     
    response=web.get('/weight-api/health')
    assert response.status_code==200

