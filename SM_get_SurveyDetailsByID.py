#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import boto3
import sys
import subprocess
import os

# pip install custom package to /tmp/ and add to path
subprocess.call('pip install requests -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')

import requests

def lambda_handler(event, context):
    # TODO implement
    
    client = requests.session()
    s3 = boto3.resource('s3')

    headers = {
    "Authorization": "bearer %s" % "f0bTPxDIDvMEn3nkrh1PWSsIutsg36RBc.Y7.WtRvUnv-Ai0nmiit-qBFmbSoDTworeCFIOBCLKXr2kiL2UAiFnQLlXvw6KToY9mXZ0fcC2fhOlIclWmPSWVa1USIOqm",
    "Content-Type": "application/json"
    }
    
    survey_list = [{'id': '284070669', 'title': 'Candidate Questionnaire', 'nickname': 'SHANGHAI D-Ford Screen + Competency Assessment', 'href': 'https://api.surveymonkey.net/v3/surveys/284070669'},
    {'id': '281634952', 'title': 'Candidate Questionnaire', 'nickname': 'D-Ford Screen + Competency Assessment', 'href': 'https://api.surveymonkey.net/v3/surveys/281634952'},
    {'id': '285767587', 'title': 'Candidate Questionnaire', 'nickname': 'Palo Alto D-Ford Screen + Competency Questionnaire', 'href': 'https://api.surveymonkey.net/v3/surveys/285767587'},
    {'id': '282632044', 'title': 'Candidate Questionnaire', 'nickname': 'Job Posting Screen', 'href': 'https://api.surveymonkey.net/v3/surveys/282632044'}]
    
    data = {}

    HOST = "https://api.surveymonkey.net"
    #SURVEY_LIST_ENDPOINT = "/v3/collectors"
    
    SURVEY_LIST_ENDPOINT = "/v3/surveys"
    
    uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)
    
    #print(uri)
    for i in survey_list:
        survey_id = i["id"]
        extra = "/details"
        new_uri  = uri + "/" + survey_id + extra
        
        print(new_uri)
        
        response = client.get(new_uri, headers=headers)
        response_json = response.json()
        
        #print(response_json)
        
        with open('/tmp/' + survey_id + "_details.json", 'w') as f:
            json.dump(response_json, f)
        

        s3.Object('surveymonkey-raw', survey_id + '/' + survey_id+ "_details.json").put(Body=open('/tmp/' + survey_id + "_details.json", 'rb'))


    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

