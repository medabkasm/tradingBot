from binance.client import Client
import binance.exceptions as expt


def sign_in(apiFile = False):

    if apiFile:
        clientStatus = False
        try:
            with open("apiKey.txt","r") as apiFile :
                (apiKeyText,apiKey) = apiFile.readline().split(":",1)
                (secretKeyText,secretKey) = apiFile.readline().split(":",1)
                print(apiKeyText)
                print(apiKey)
                print(secretKeyText)
                print(secretKey)
        except IOError as ioError:
            print('Error :: File : {} .'.format(str(ioError)))
            return False

        if apiKeyText == "API_KEY" and secretKey == "SECRET_KEY" :
            try:
                client = Client(apiKey.rstrip(),secretKey.rstrip())
                clientStatus = True

            except:
                print(' Error : Account can''t be opened correctelly .')
                pass
        else:
            print('Error : File structure is not correct .')
            print('You need to enter your api key and secret key manually .')
            apiKey = input('API KEY : ')
            secretKey = input('SECRET KEY : ')
            client = Client(apiKey.rstrip(),secretKey.rstrip())

    else:
        apiKey = input('API KEY : ')
        secretKey = input('SECRET KEY : ')
        try:
            client = Client(apiKey.rstrip(),secretKey.rstrip())
            clientStatus = True

        except:
            print(' Error :: Account can''t be opened be opened correctelly . ')
            pass

    status = client.get_system_status()
    if(status['status'] == 1 ):
        print('Error :: System Status : '+ status['msg'])
        return False
    else:
        try:
            state = client.get_account()
        except expt.BinanceAPIException as err:
            print('Error :: '+str(err) + '.')
        except expt.BinanceRequestException as err:
            print('Error :: '+str(err) + '.')

        return client
