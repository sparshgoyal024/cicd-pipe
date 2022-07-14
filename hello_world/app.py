import json
import pandas as pd
import time
import os
import pickle
import boto3

def lambda_handler(event, context):

    fn_start_time = time.time()

    wiki_url='https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'

    time.sleep(5) #seconds consider as minute just for testing, same logic works for minutes 
    diff_time = (time.time() - fn_start_time)
    dynamodb = boto3.client('dynamodb') #Init DynamoDB Client

    if not os.path.isfile("/tmp/rank.txt"): # Checking if state file file exists or not 
        df=pd.read_html(wiki_url, header=0)[0]  # Reading the URL using Pandas
        df = df[['Rank']] # Using DataFrames
        number = df.head(200).to_string(index=False).split("\n") 
        resume_number = 1 # Starting Index
        n=0 # Counter
    else:
        infile = open("/tmp/rank.txt",'rb') #Opening State file in read binary mode
        number = pickle.load(infile) #Actual Rank
        infile.close()
        index = open("/tmp/state.txt",'rb') 
        resume_number = pickle.load(index) #Reading Resume Index if function is executed again
        n=resume_number
        infile_no.close()

    for rank in number[resume_number::]:

        if (time.time() - start_time) < 10:
            rank_file = open("/tmp/rank.txt",'wb') 
            pickle.dump(number,rank_file) #Storing the Rank
            rank_file.close()
            state_file = open("/tmp/state.txt",'wb')
            n = resume_number + 1
            pickle.dump(n,state_file) #Storing the State
            state_file.close()
            dynamodb.put_item(TableName='wiki', Item={'rank':{'S':rank}})

        else:
            break
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Function Executed Completed",
        }),
    }
