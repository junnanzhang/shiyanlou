import re 
from datetime import datetime
import collections

def open_parser(filename):
  with open(filename) as logfile:
    pattern = (r''
               r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP ??
               r'\[(.+)\]\s'  # ??
               r'"GET\s(.+)\s\w+/.+"\s'  # ????
               r'(\d+)\s'  # ???
               r'(\d+)\s'  # ????
               r'"(.+)"\s'  # ???
               r'"(.+)"'  # ?????
               )
    parsers = re.findall(pattern, logfile.read())
  return parsers

def main():
  logs = open_parser('/home/shiyanlou/Code/nginx.log')
  ips = []
  get404 = []
  for item in logs:
    if item[1][:11] == '11/Jan/2017':
      ips.append(item[0])
    if item[3] == '404':
      get404.append(item[2])


  most = collections.Counter(ips)
  mostip = most.most_common(1)[0]
  ip_dict = {mostip[0]:mostip[1]}

  mostUrl = collections.Counter(get404)
  topUrl = mostUrl.most_common(1)[0]
  url_dict = {topUrl[0]:topUrl[1]}
  return ip_dict, url_dict


if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)