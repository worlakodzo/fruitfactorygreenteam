import requests
base_url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8086'


def test_home_page():    
    response=requests.get(base_url)
    assert response.status_code==200
    

    # get_home_response=[{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10001,"neto":500,"produce":"oranges","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10002,"neto":500,"produce":"oranges","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10003,"neto":500,"produce":"apples","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10004,"neto":500,"produce":"apples","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10005,"neto":500,"produce":"banana","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10006,"neto":500,"produce":"banana","truck":"t0001","truckTara":500}]
    # assert response==get_home_response
    # get_weight_in_response=[{"bruto":1000,"containers":"abcde","direction":"in","id":10001,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"in","id":10003,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"in","id":10005,"neto":500,"produce":"banana"}]
    # get_weight_out_response=[{"bruto":1000,"containers":"abcde","direction":"out","id":10002,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"out","id":10004,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"out","id":10006,"neto":500,"produce":"banana"}]
     