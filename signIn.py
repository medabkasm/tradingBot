def sign_in():
    try:
        apiFile = open('api.txt','r')
        apiKey = apiFile.readline(1)
        secretKey = apiFile.readline(2)
    except:
        print('Error while reading the api file ')
        return False

    try:
        client = Client(apiKey,secretKey)
    except:
        print('Error : can''t sign in ')
        return False

    status = client.get_system_status()
    if(status['status']):
        print(status['msg'])
        return False
    else:
        return client
