import requests #importing the requests module to handle HTTP requests
import argparse #Importing argparse to handle command-line arguments
import sys #Importing sys to access command-line arguments and standard input
from urllib.parse import urlparse #importing urlparse to handle URL parsing

#enum function to ensure the url has a scheme (htpp:// or https://) 
def enum(url):
    #if the URL doesn't have a scheme e.g http://
    if not urlparse(url).scheme:
        return "http://" + url
    return url

#function to perform brute-force directory enumeration on a given base url
def brute(base_url, wordlist):
    #ensure the base_url has a valid scheme using the enum function
    base_url = enum(base_url)

    #if the base URL does not end with a "/", add it to form proper URLs
    if not base_url.endswith("/"):
        base_url += "/"

#iterate over each word in the wordlist
    for word in wordlist:
        #construct the full URL by appending the stripped word to the base URL
        url = base_url + word.strip()

        try:
            #attempt to send Get request to the constructed URL with a 1-second timeout
            response = request.get(url, timeout=1)

            #if the server responds with a status code 200, it means the URL was found
            if response.status_code == 200:
                print(f"found {url}")
            else:
                #if the URL is not found (or other non-200 status), print the status code
                print(f"Not found {url} {response.status_code}")
                
        #if the request times out, print a timeout message
        except requests.exceptions.Timeout:
            print(f"Timeout with {url}")

        #if there is a connection error (e.g., DNS failure, refused connection), print a failed to connect message
        except requests.ConnectionError:
            print(f"Failed to Connect {url}")

#create an argumentparser object to handle command-line arguments
parser = argparse.ArgumentParser()

#add a positional command-line argument called "base_url"
parser.add_argument("base_url")

#Parse the command-line arguments and store them in the args object
args = parser.parse_args()

#read the wordlist from standard input (e.g., a file or piped input)
wordlist = [line for line in sys.stdin]

#call the brute function, passing the base URL and the wordlist as arguments
brute(args.base_url, wordlist)