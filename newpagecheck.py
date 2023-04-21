#new page check
import csv
import concurrent.futures
import requests
import sys
try:
    # get the input parameters from the command line
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print('failed to get successful parameters')

# open the input file and read the URLs
with open(input_file, 'r') as input_csv:
    reader = csv.reader(input_csv)
    urls = [row[0] for row in reader]

# check if each URL is valid using multiple threads
invalid_urls = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    # send a GET request to each URL
    responses = {executor.submit(requests.get, url): url for url in urls}
    for response in concurrent.futures.as_completed(responses):
        url = responses[response]
        print(url)
        print(response)
        try:
            # if the response status code is not 200 (OK), the URL is invalid
            if response.result().status_code != 200:
                invalid_urls.append(url)
        except requests.ConnectionError:
            # if there was a connection error, the URL is invalid
            invalid_urls.append(url)
        except:
            invalid_urls.append(url)

# write the invalid URLs to the output file
with open(output_file, 'a',newline='') as output_csv:
    writer = csv.writer(output_csv)
    for row in invalid_urls:
        writer.writerow([row])
   
