#!/usr/local/bin/python3
# cs432-hw1.py

import requests
import re 
import sys
from bs4 import BeautifulSoup

# returns a list of links
def find_pdf(uri):
  resp = requests.get(uri)  
  # Pattern that matches pdf files
  pattern = re.compile('([^&]+pdf)')  
  my_list = []
  # Find all links
  soup = BeautifulSoup(resp.text)
  for links in soup.find_all('a'):
    href = links.get('href')
    m = pattern.match(href)
    if (m!= None):
      new_uri = m.groups()[0]
      my_list.append(new_uri)

  return my_list

# returns a int of bytes
def content_len(uri):
  attr = 'Content-Length'
  resp = requests.get(uri)
  return (attr +': ' + resp.headers[attr] + ' bytes\n')

# check the headers
def check_headers(uri):
  response = requests.get(uri)
  return response.headers

# return a string with the final destination after reroutes
def get_final_uri(uri):
  response = requests.get(uri)
  if response.history:
    return ('Final Destination: ' + str (response.url))
  else:
    return ('Final Destination: ' + str (uri))

def main(args=None):
  try:
    arg = sys.argv[1]
  except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <URL>")
  print (arg[::-1])
  
  # testing url
  #url = 'https://www.cs.odu.edu/~mweigle/courses/cs532/pdfs.html'
  url = arg
  uri_list = find_pdf(url)
  for link in uri_list:
    print ('URI: ' + link)
    print (get_final_uri(link))
    print (content_len(link))

if __name__ == "__main__":
    main()