import requests
base_url = 'http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8081'

def test_weight():    
    response=requests.get(f'{base_url}/weight')
    assert response.status_code==200
    # get_weight_res=[{"bruto":1000,"containers":"abcde","direction":"in","id":10001,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"out","id":10002,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"in","id":10003,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"out","id":10004,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"in","id":10005,"neto":500,"produce":"banana"},{"bruto":1000,"containers":"abcde","direction":"out","id":10006,"neto":500,"produce":"banana"},{"bruto":120,"containers":"K-7567,C-1265","direction":"in","id":10007,"neto":null,"produce":"orange"}]
    # assert response.json==get_weight_res
    
def test_weight_with_filter_in(): 
    response=requests.get(f'{base_url}/weight?filter=in')
    assert response.status_code==200

def test_weight_with_filter_out():   
    response=requests.get(f'{base_url}/weight?filter=out')
    assert response.status_code==200

    # get_home_response=[{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10001,"neto":500,"produce":"oranges","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10002,"neto":500,"produce":"oranges","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10003,"neto":500,"produce":"apples","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10004,"neto":500,"produce":"apples","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"in","id":10005,"neto":500,"produce":"banana","truck":"t0001","truckTara":500},{"bruto":1000,"containers":"abcde","datetime":"Sat, 01 Jan 2022 12:24:56 GMT","direction":"out","id":10006,"neto":500,"produce":"banana","truck":"t0001","truckTara":500}]
    # assert response==get_home_response
    # get_weight_in_response=[{"bruto":1000,"containers":"abcde","direction":"in","id":10001,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"in","id":10003,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"in","id":10005,"neto":500,"produce":"banana"}]
    # get_weight_out_response=[{"bruto":1000,"containers":"abcde","direction":"out","id":10002,"neto":500,"produce":"oranges"},{"bruto":1000,"containers":"abcde","direction":"out","id":10004,"neto":500,"produce":"apples"},{"bruto":1000,"containers":"abcde","direction":"out","id":10006,"neto":500,"produce":"banana"}]
     