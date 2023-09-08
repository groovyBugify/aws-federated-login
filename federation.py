import urllib, json, sys
import requests # 'pip install requests'

# Step 1: Enter the session credentials
access_key_id = input('Enter Access Key ID: ')
secret_access_key = input('Enter Secret Access Key: ')
session_token = input('Enter Session Token: ')

# Step 2: Format resulting temporary credentials into JSON
url_credentials = {}
url_credentials['sessionId'] = access_key_id
url_credentials['sessionKey'] = secret_access_key
url_credentials['sessionToken'] = session_token
json_string_with_temp_credentials = json.dumps(url_credentials)

# Step 3. Make a request to the AWS federation endpoint to get a sign-in token. Construct the parameter string with the sign-in action request, a 12-hour session duration, and the JSON document with temporary credentials as parameters.

request_parameters = "?Action=getSigninToken"
request_parameters += "&SessionDuration=43200"
if sys.version_info[0] < 3:
    def quote_plus_function(s):
        return urllib.quote_plus(s)
else:
    def quote_plus_function(s):
        return urllib.parse.quote_plus(s)
request_parameters += "&Session=" + quote_plus_function(json_string_with_temp_credentials)
request_url = "https://signin.aws.amazon.com/federation" + request_parameters
r = requests.get(request_url)
# Returns a JSON document with a single element named SigninToken.
signin_token = json.loads(r.text)

# Step 4: Create a URL where users can use the sign-in token to sign in to  the console. This URL must be used within 15 minutes after the sign-in token was issued.

request_parameters = "?Action=login" 
request_parameters += "&Issuer=Example.org" 
request_parameters += "&Destination=" + quote_plus_function("https://console.aws.amazon.com/")
request_parameters += "&SigninToken=" + signin_token["SigninToken"]
request_url = "https://signin.aws.amazon.com/federation" + request_parameters

# Send final URL to stdout
print ('''\r\n
********************************************
* The URL to log in to the AWS console is: *
********************************************''') 
print(request_url)
