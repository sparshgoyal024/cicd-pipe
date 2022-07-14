import json
import pandas as pd
import time
import os
import pickle
import boto3

def lambda_handler(event, context):

    start_time = time.time()

    url='https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'

    time.sleep(4) #seconds consider as minute just for testing, same logic works for minutes 
    execute = (time.time() - start_time)
    dynamodb = boto3.client('dynamodb')
    #print(execute)



    if not os.path.isfile("/tmp/state.txt"):
        #outfile = open(state_file,'x')
        df=pd.read_html(url, header=0)[0]
        df = df[['Rank']]
        number = df.head(200).to_string(index=False).split("\n")
        #print(number)
        resume_number = 1
        n=0
        #print("if")
    else:
        infile = open("/tmp/state.txt",'rb')
        number = pickle.load(infile)
        infile.close()
        infile_no = open("/tmp/state1.txt",'rb')
        resume_number = pickle.load(infile_no)
        #print("he",resume_number)
        n=resume_number
        #print("else")
        infile_no.close()

    for rows in number[resume_number::]:
        #print(rows)

        #print("hllo")

        #print(time.time() - start_time) # ~5
        if (time.time() - start_time) < 7:

            time.sleep(1)
            outfile = open("/tmp/state.txt",'wb')
            pickle.dump(number,outfile)
            outfile.close()
            outfile1 = open("/tmp/state1.txt",'wb')
            n = resume_number + 1
            pickle.dump(n,outfile1)
            outfile1.close()
            print(rows)
            dynamodb.put_item(TableName='wiki', Item={'rank':{'S':rows}})

        else:
            print("Test")
            break
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
