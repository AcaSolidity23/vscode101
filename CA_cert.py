import os
import sys
import certifi
import requests as r
print(r.certs.where())
print (str(certifi.where()))


os.environ['SSL_CERT_FILE'] = r.certs.where()
#os.environ['SSL_CERT_FILE'] = str(certifi.where())

os.environ['REQUESTS_CA_BUNDLE'] =
os.path.join(os.path.dirname(sys.argv[0]), certifi.where())
