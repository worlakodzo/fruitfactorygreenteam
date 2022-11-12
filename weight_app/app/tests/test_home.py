from app import app
def test_home_page():
    flask_app=create_app('flask_test.cfg')

    with flask_app.test_client() as test_client:
        response=test_client.get('/')
        assert response.status_code==200
        assert b'truckTara' in response.data