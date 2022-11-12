from app import app


def test_item_withId():
    web=app.test_client()     
    response=web.get('/item/t0001')
    assert response.status_code==200

def test_item_withoutId():
    web=app.test_client()     
    response=web.get('/item')
    assert response.status_code==404