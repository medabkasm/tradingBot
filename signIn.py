from binance.client import Client
import binance.exceptions as expt


def sign_in(apiFile = False ,fileName = None):


    accountStatus = {'loginStatus':'standard' ,  # standard  user not signed in , or  signed in for signed
                        'fileStatus':'not used' ,
                        'system':'normal',  # for binance system , normal or maintenance
                        'account':None,
                        'apiStatus' : 'no exceptions '  # api status , exceptions occurs
                    }  #   holds the client object , None for empty object , client for signed in
    if apiFile:
        try:
            with open(fileName,"r") as apiFile :
                (apiKeyText,apiKey) = apiFile.readline().split(":",1)
                (secretKeyText,secretKey) = apiFile.readline().split(":",1)
                print(apiKeyText + ' : ' + apiKey)
                print(secretKeyText + ' : ' + secretKey)
                accountStatus['fileStatus'] = 'used'

        except IOError as ioError:
            accountStatus['fileStatus'] = 'Error :: '+ str(ioError)
            return accountStatus

        if apiKeyText == "API_KEY" and secretKeyText == "SECRET_KEY" :
           client = Client(apiKey.rstrip(),secretKey.rstrip())

        else:
            print('Error : File structure is not correct .')
            print('You need to enter your api key and secret key manually .')
            apiKey = input('API KEY : ')
            secretKey = input('SECRET KEY : ')
            client = Client(apiKey.rstrip(),secretKey.rstrip())

    else:
        apiKey = input('API KEY : ')
        secretKey = input('SECRET KEY : ')
        client = Client(apiKey.rstrip(),secretKey.rstrip())

    status = client.get_system_status()
    if(status['status'] == 1 ):
        accountStatus['apiStatus'] = status['msg']
        return accountStatus
    else:
        try:
            state = client.get_account()
            accountStatus['loginStatus'] = 'signed'
            accountStatus['account'] = client

        except expt.BinanceAPIException as err:
            accountStatus['apiStatus'] = str(err)
            return accountStatus
        except expt.BinanceRequestException as err:
            accountStatus['apiStatus'] = str(err)
            return accountStatus

    print(' Account :: signed in succesfully .')
    return accountStatus
