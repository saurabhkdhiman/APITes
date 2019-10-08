'''
Created on 24-Aug-2018

@author: S Kumar
'''
import requests
import random
from json import dumps
import pytest


@pytest.fixture
def test_getFreewayEnv():
    configuration = {"staging": {"host":"https://qafreewayapis.syntoniccsp.com/scspsd/v2/","cCode":"91","devKey":"ad47013b-57be-4e08-a5ab-6e39c2398e60","sdkhost":"https://fbapis.syntoniccsp.com/freeway/sdk/v.122316/","version": "2.0.53"},"production": {"host":"https://apis.freeway.syntonic.com/scspsd/v2/","cCode":"91","devKey":"f35396dc-fbae-4d1e-89e5-fd61748781e2","sdkhost":"https://apis.freewaysdk.syntoniccsp.com/freeway/sdk/v.122316/","version": "2.6.8"}}
#     getInput  = ''
#     while getInput !='1' and  getInput != '0':
#         getInput = input("Please enter '0' for staging and '1' for prodcution : \n")
#     if getInput == '0':
#         mode = "staging"
#     else:
#         mode = "production"
    mode = "staging"    
    hostUrl = configuration[mode]["host"]
    countryCode=configuration[mode]["cCode"]
    #DevKey = configuration[mode]["devKey"]
    #hostSDKUrl = configuration[mode]["sdkhost"]
    appVersion = configuration[mode]["version"]
    startDigit = "111111"
    lastDigit = random.randint(1000,9999)
    phoneNumber = startDigit + str(lastDigit)
    #headers = {"platform":"ANDROID"}
    
    return hostUrl,countryCode,appVersion,phoneNumber

@pytest.fixture
def test_getSDKEnv():
    configuration = {"staging": {"host":"https://qafreewayapis.syntoniccsp.com/scspsd/v2/","cCode":"84","devKey":"ad47013b-57be-4e08-a5ab-6e39c2398e60","sdkhost":"https://fbapis.syntoniccsp.com/freeway/sdk/v.122316/","version": "2.0.53"},"production": {"host":"https://apis.freeway.syntonic.com/scspsd/v2/","cCode":"91","devKey":"f35396dc-fbae-4d1e-89e5-fd61748781e2","sdkhost":"https://apis.freewaysdk.syntoniccsp.com/freeway/sdk/v.122316/","version": "2.6.8"}}
#     getInput  = ''
#     while getInput !='1' and  getInput != '0':
#         getInput = input("Please enter '0' for staging and '1' for prodcution : \n")
#     if getInput == '0':
#         mode = "staging"
#     else:
#         mode = "production"
    mode = "staging"    
    #hostUrl = configuration[mode]["host"]
    #countryCode=configuration[mode]["cCode"]
    DevKey = configuration[mode]["devKey"]
    hostSDKUrl = configuration[mode]["sdkhost"]
    #appVersion = configuration[mode]["version"]
    #startDigit = "111111"
    #lastDigit = random.randint(1000,9999)
    #phoneNumber = startDigit + str(lastDigit)
    headers = {"platform":"ANDROID"}
    
    return hostSDKUrl,DevKey,headers
    

token= ""
newPhoneNumber=""
headers = {"platform":"ANDROID"}
getsponsoredOfferId=""

#For reward specific
getRewardId=""
getClaimId=""
getConversionUrlfromClaimReward=""

@pytest.mark.smoke
def test_authenticate(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    authenticateAPI= requests.post(f"{hostUrl}authenticate", {"phoneNumber": phoneNumber,"countryCode":countryCode,"advertiserId":"","deviceSecret":"","appVersion":appVersion,"imei":"","isRootDevice":False,"clevertapId":"","platform":"ANDROID"},headers=headers)
    A=authenticateAPI.json()
    global newPhoneNumber
    if 'token' not in A:
        assert authenticateAPI.status_code == 200
        assert A['message'] == 'Authentication process initiated'
        #print(A)
        newPhoneNumber=phoneNumber
    elif 'token' in A: 
        assert authenticateAPI.status_code == 200
        #print(A)
        global token
        token = A['token']
        newPhoneNumber=phoneNumber      

@pytest.mark.smoke  
def test_verifyCode(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    lastDigit=newPhoneNumber[6:10]
    #print(lastDigit)
    verifyCode= requests.post(f"{hostUrl}verifyCode", {"phoneNumber": newPhoneNumber,"countryCode":countryCode,"code":lastDigit,"deviceSecret":"","clevertapId":"__g6f5c5986405e48a5b42b408fc6211824"},{'platform':'ANDROID'})
    assert verifyCode.status_code == 200
    vcodeResponse = verifyCode.json()
    assert vcodeResponse['isCountrySupported']==True
    #print (vcodeResponse)
    global token 
    token = vcodeResponse['token']
@pytest.mark.smoke
@pytest.mark.xfail

def test_setMetaData(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    setMetaData = requests.post(f"{hostUrl}setMetaData", {"token": token,"locale":"en","extraInfo": {"deviceLocale":"en-GB"},"platform":"ANDROID","appVersion":"2.0.51","operator":{"operatorId":3006,"roamingState":False,"operatorMCC":"404","operatorMNC":"10","networkMCC":"404","networkMNC":"10"},"device":{"version":"6.0","brand":"motorola"}},{'platform':'ANDROID'})
    #getMetaDataResponse = setMetaData.json()
    #print(getMetaDataResponse)
    assert setMetaData.status_code == 200
        
@pytest.mark.smoke
@pytest.mark.xfail
def test_setNetworkInfo(test_getSDKEnv):
    hostSDKUrl,DevKey,headers=test_getSDKEnv
    setNetworkInfo = requests.post(f"{hostSDKUrl}setNetworkInfo", {"devKey": DevKey, "userId":"593109", "oldUserId":"d3ee2155-0140-4e00-bd80-12fefd0adaba","phone": newPhoneNumber, "networkMCC": "404", "networkMNC": "10", "operatorMCC": "404", "operatorMNC": "10", "connectionType": "WWAN", "roamingState":False, "deviceUniqueId":"5a619617-c917-423d-a3b1-21d1a0063a9e", "osUserId": "560bfc00bbef9464"}, headers=headers)
    getNetworkResponse = setNetworkInfo.json()
    assert setNetworkInfo.status_code == 200
    assert getNetworkResponse["type"]=='SPONSORED'
    assert getNetworkResponse["isEligible"] == True
    
#h = dumps(getNetworkResponse)
#print(h)
# 
# print(f'setNetworkInfo response status: {setNetworkInfo.status_code}')

@pytest.mark.smoke
def test_getContentCatalogue(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    getContentCatalogue = requests.get(f"{hostUrl}getContentCatalogue?token={token}",  headers=headers)
    contentCatalogueResponse=getContentCatalogue.json()
    #print(contentCatalogueResponse)
    #print(getContentCatalogue.headers)
    assert getContentCatalogue.status_code == 200
    global getsponsoredOfferId
    global getRewardId 
    if len(contentCatalogueResponse["campaigns"]) !=0:
        getsponsoredOfferId=contentCatalogueResponse["campaigns"][0]["id"]
        #print(f"1. Sponsored offer: {getsponsoredOfferId}")
    else:
        print("1. Sponsored Offer: There is no sponsored offer available")
        getsponsoredOfferId = 0     
    if len(contentCatalogueResponse["rewards"]) !=0:
        getRewardId=contentCatalogueResponse["rewards"][0]["id"]
        #print(f"2. Reward: {getRewardId}")
    else:
        print("2. Reward: There is no reward available")
        getRewardId = 0    
 
# alpha1 = dumps(contentCatalogueResponse)
# print (alpha1)
# 
# print(F"getContentCatalogueResponse status: {getContentCatalogue.status_code}")
# 
# '''
# print(f'getContentCatalogue response status: {getContentCatalogue.status_code}')                                                                                            
# 
# 
@pytest.mark.smoke 
def test_claimSponsoredOffer(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    if getsponsoredOfferId !=0:
        claimCampaign=requests.post(f"{hostUrl}claimCampaign", {"id":getsponsoredOfferId,"token":token,"clientAnchorTime":"","serverAnchorTime":"","clientCurrentTime":"","isUnsignedApp":False})
        claimCampaignResponse=claimCampaign.json()
        assert claimCampaign.status_code == 200
        assert 'claimedOn' in claimCampaignResponse
    elif getsponsoredOfferId ==0:
        print("There is not sponsored offer for claim")

@pytest.mark.smoke
def test_claimReward(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    if getRewardId !=0:
        claimReward = requests.post(f"{hostUrl}claimReward", {"id":getRewardId,"token":token,"clientAnchorTime":"","serverAnchorTime":"","clientCurrentTime":"","isUnsignedApp":False})
        claimRewardResponse=claimReward.json()
        assert claimReward.status_code == 200
        assert 'claimedOn' in claimRewardResponse
        global getClaimId
        getClaimId=claimRewardResponse["claimId"]
        global getConversionUrlfromClaimReward
        getConversionUrlfromClaimReward=claimRewardResponse["conversionUrl"]
        #print(claimRewardResponse)
    elif getRewardId == 0:
        print("There is no reward for claim")    
        
@pytest.mark.smoke 
def test_rewardStatus(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    getRewardStatus = requests.get(f"{hostUrl}getRewardStatus?token={token}&ids={getClaimId}",  headers=headers)
    getRewardStatusResponse =getRewardStatus.json()
    assert getRewardStatusResponse['rewards'][0]['status']
    
@pytest.mark.smoke
def test_getConversionUrl(test_getFreewayEnv):
    getConversionUrl=requests.get(f"{getConversionUrlfromClaimReward}&clientAnchorTime=1530183029&serverAnchorTime=1530183029&clientCurrentTime=1530183029")
    #print(getConversionUrl.json())
    assert getConversionUrl.status_code == 200
@pytest.mark.smoke
def test_getTopupDenomination(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    getTopupDenomination=requests.get(f"{hostUrl}getTopupDenominations?token={token}")
    #print(getTopupDenomination.json())
    assert getTopupDenomination.status_code
    
# ''' 
@pytest.mark.smoke        
def test_topup(test_getFreewayEnv):
    hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv
    getTopup=requests.post(f"{hostUrl}topup", {"token":"d9f068bf-b871-4e9a-8962-dca45a9411b5","id":"353","type":"1","amount":"10"})
    print(getTopup.json())        
        
        
        
        
# def test_setNativeUsage(test_getFreewayEnv):
#     hostUrl,countryCode,appVersion,phoneNumber = test_getFreewayEnv 
#     setNativeUsage = requests.post(f"{hostUrl}setNativeUsage", {"token": token,"subscriptionUsage": {"sponsoredUsage": [{"timestamp":"2017-05-21T12:51:36.452Z","subscriptionId": 131,"usage": {"269": {"downlinkBytes": 1,"uplinkBytes": 1},"316":{"downlinkBytes": 2,"uplinkBytes": 2},"350": {"downlinkBytes": 3,"uplinkBytes": 3}}}],"nonSponsoredUsage": {"wwan": [{"timestamp": "2017-05-21T12:51:36.452Z","subscriptionId": 131,"usage": {"269": {"downlinkBytes": 1,"uplinkBytes": 1},"316": {"downlinkBytes": 2,"uplinkBytes": 2},"350": {"downlinkBytes": 3,"uplinkBytes": 3}}}],"wlan": [{"timestamp":"2017-05-21T12:51:36.452Z","subscriptionId": 131,"usage": {"269": {"downlinkBytes": 1,"uplinkBytes": 1},"316": {"downlinkBytes": 2,"uplinkBytes": 2},"350": {"downlinkBytes": 3,"uplinkBytes": 3}}}]}},"sponsoredUsage": [],"nonSponsoredUsage": {"wwan": [],"wlan": []}}, headers=headers)
#     print(setNativeUsage.json())
# 

# '''
# topupToken=input("Please enter token for topup: ")
# print(topupToken)
#     
# 
# 
# #getTopup=requests.post(f"{hostUrl}topup", {"token":"d9f068bf-b871-4e9a-8962-dca45a9411b5","id":"353","type":"1","amount":"10"})
# #print(getTopup.json())
# '''