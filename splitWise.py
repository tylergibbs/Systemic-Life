from splitwise import Splitwise
import os
import re
import json

class SplitWise(Splitwise):
     def __init__(self, key, secret):
         super().__init__(key, secret)

         credentialDir = os.path.join(os.path.expanduser('~'), '.credentials')
         if not os.path.exists(credentialDir):
              os.makedirs(credentialDir)
         credential_path = os.path.join(credentialDir, 'splitwise-life-manadgement.json')
         if not os.path.exists(credential_path):
            url, secret = self.getAuthorizeURL()
            print(url)
            print("enter oauth_verifier")
            oauth_verifier = input().strip()
            oauth_token    = re.findall("https://secure.splitwise.com/authorize\?oauth_token=(.+)", url)[0]
            access_token = self.getAccessToken(oauth_token, secret, oauth_verifier)
            print(access_token)
            f = open(credential_path, 'w')
            json.dump(access_token, f)
            f.close()
         else:
            f = open(credential_path, 'r')
            access_token = json.load(f)
            f.close()
         self.setAccessToken(access_token)
