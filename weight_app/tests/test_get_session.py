from app import app


def test_session():
    web=app.test_client()     
    response=web.get('/session/10001')
    assert response.status_code==200

def test_session_withoutId():
    web=app.test_client()     
    response=web.get('/session')
    assert response.status_code==404