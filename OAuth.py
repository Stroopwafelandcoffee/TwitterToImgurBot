import requests
import pprint
 
#https://api.imgur.com/oauth2#auth_url
def getPin(client_id, client_secret):
    """build a URL for the user to navigate to and "Allow" the application"""
 
    resp = "pin"
    #can be any string at all
    state = "anything"
    url = r"https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}"
 
    print("browse to the following URL and grab the pin:")
    pin_url = url.format(cid=client_id,resp= resp, app_state=state)
    print(pin_url)
 
    return(pin_url)
 
def exchangePinForTokens(client_id, client_secret, pin):
    """takes the client_id and client_secret from the registered application URL,
    along with the pin returned from `getPin()`, and return an access_token and a
    refresh_token"""
 
    #the query parameters you'll send along with the POST request
    params ={ "client_id" : client_id,
             "client_secret" : client_secret,
             "grant_type" : "pin",
             "pin": pin}
 
    url = r"https://api.imgur.com/oauth2/token/"
 
    #make sure the data is sent with the POST request, along with disabling the
    # SSL verification, potential security warning
    r = requests.post(url, data = params, verify=False)
    j= r.json()
    print("The exchangePinForTokens API response:")
    pprint.pprint(j)
 
    #add the access_token to the headers as
    # Authorization: Bearer YOUR_ACCESS_TOKEN
    access_token= j['access_token']
    refresh_token= j['refresh_token']
    print("Access Token: {0}\nRefresh Token: {1}".format(access_token,
            refresh_token))
 
    return (access_token, refresh_token)
 
def uploadImage(access_token, image_url):
    """uploads an image using it's URL, the access_token is required"""
 
    #need to include the authorization headers,
    # in order to make use of the access token
    headers = {"authorization":"Bearer {0}".format(access_token)}
 
    upload_url = r'https://api.imgur.com/3/upload'
 
    #this is the data we'll POST to the api's URL
    payload = {'image' : image_url,
                'type':'url',
                'title':"WORKS"}
 
    #make the upload, ensuring that the data, headers are included, and
    # make sure to disable the verification of the SSL. Potential insecurty though
    r = requests.post(upload_url, data=payload, headers=headers, verify=False)
 
    #save the json response, print it to screen
    j = r.json()
    print("The UploadImage API response:")
    pprint.pprint(j)
 
    #print the img URL to verify that the image is still  there
    uploaded_url = j['data']['link']
    print("The uploaded image URL is: {0}".format(uploaded_url))
 
#a popular Python idiom to make sure that the following code gets run when this
# file is ran as __main__, rather than imported
if __name__ == '__main__':
    """Run the following if module is top module"""
 
    #found here: https://api.imgur.com/oauth2/addclient
    client_id= #**
    client_secret= #**
 
    image_url = r'http://www.personal.psu.edu/afr3/blogs/siowfa12/success.jpeg'
 
    #URL needed to have the user visit and allow the application to use the pin
    getPin(client_id,client_secret)
    pin = input("input PIN\n")
 
    access_token, refresh_token = exchangePinForTokens(client_id,client_secret,pin)