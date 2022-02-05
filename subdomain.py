from googlesearch import search
import argparse
from urllib.parse import urlparse

domains = set()

# defining the parse to send the domain as argument from CLI
parser = argparse.ArgumentParser(prog="Dorker plus", description="Recon using the Google search")
parser.add_argument('-d', action='store', dest='domain',
                    help='domain: <vulnerablewebsite.com> you dont have to send the protocol')
parser.add_argument('-o', action='store', dest='output', help='path of the output file')

# Storing the arguments in a variable to access across the program
args = parser.parse_args()
if args.domain is None:
    print("Please enter the domain you wish to target: subdomain.py -d target.com")
    exit()
else:
    domain = args.domain

dork = "site:*." + domain + " -inurl:www"


# To clear the Google cookie to prevent HTTP code 429 Too many requests
def clear_cookie():
    fo = open(".google-cookie", "w")
    fo.close()


# Dork function to fetch the subdomains
def dorker():
    global dork
    for i in range(2):
        for sub in search(dork, stop=200):
            domains.add(urlparse(sub).hostname)
            dork = dork + " -inurl:" + urlparse(sub).hostname
            clear_cookie()
        [print(x+'\n') for x in domains]


# Print the output in a file
def output():
    file = open(args.output, 'w')
    [file.write(x + '\n') for x in domains]
    file.close()


dorker()
if args.output is not None:
    output()
