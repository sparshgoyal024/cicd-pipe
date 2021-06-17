import json
import pandas as pd
import time
import os
import pickle
import boto3

def lambda_handler(event, context):
    start_time = time.time()

    url='https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'

    state_file = '/tmp/state.txt'
    no_file = '/tmp/state1.txt'

    time.sleep(1.56978)
    execute = (time.time() - start_time)
    dynamodb = boto3.client('dynamodb')



    if not os.path.isfile("/tmp/state.txt"):
        df=pd.read_html(url, header=0)[0]
        df = df[['Rank']]
        number = df.head(200).to_string(index=False).split("\n")
        resume_number = 1
        n=0
    else:
        infile = open(state_file,'rb')
        number = pickle.load(infile)
        infile.close()
        infile_no = open(no_file,'rb')
        resume_number = pickle.load(infile_no)
        n=resume_number
        infile_no.close()

    for rows in number[resume_number::]:
        n += 1
        if (time.time() - start_time) > 1:
            print(rows)
            dynamodb.put_item(TableName='wiki', Item={'rank':{'S':rows}})
            outfile = open(state_file,'wb')
            pickle.dump(number,outfile)
            outfile.close()
            outfile1 = open(no_file,'wb')
            pickle.dump(n,outfile1)
            outfile1.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
