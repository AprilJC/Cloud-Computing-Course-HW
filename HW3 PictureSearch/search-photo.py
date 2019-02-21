import json
import boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    # q = "show me photos with City in them"
    q = event["q"]
    
    # Disambiguate the query using Lex
    lex = boto3.client('lex-runtime')
    lex_response = lex.post_text(
        botName='ImageSearch',
        botAlias='Prod',
        userId="search-photos", #unstructured['id'],
        inputText=q
    )
    print(lex_response)
    
    keywords = []
    keyWordOne = lex_response['slots']['KeyOne']
    keyWordTwo = lex_response['slots']['KeyTwo']
    if keyWordOne is not None:
        keywords.append(keyWordOne)
    if keyWordTwo is not None:
        keywords.append(keyWordTwo)
    return(keywords)
    
    # Search the keywords in ElasticSearch
    results = []
    if len(keywords) <= 2:  
        for keyword in keywords:
            host = "https://search-photo-3t6bz7diw35p6bwdhbt4m5txwm.us-east-1.es.amazonaws.comm"
            search_url = host + "/searchphotos/_search?q=" + keyword
            response = requests.get(search_url)
            response = response.json()
            for hit in response["hits"]["hits"]:
                _source = hit["_source"]
                objectKey = _source["objectKey"]
                bucket = _source["bucket"]
                labels = _source["labels"]
                result = {"url": "https://s3.amazonaws.com/" + bucket + "/" + objectKey, "labels": labels}
                results.append(result)
        return {
            'statusCode': 200,
            'body': json.dumps({"results": results})
        }
    else:  # Something wrong inside Lex
        return {
            'statusCode': 400,
            'body': lex_response["message"]
        }