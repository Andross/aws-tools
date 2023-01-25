import ssl, OpenSSL
import socket
from OpenSSL.crypto import load_certificate, FILETYPE_PEM

socket.setdefaulttimeout(5)

ssl_version=ssl.PROTOCOL_TLSv1_1
domainNameList=[""]

for domain in domainNameList:
    print(domain)
    with open('/home/oddcron/dev/aws-tools/domains.txt', 'r+') as f:
        for line in f:
            try:
                
                new_domain = line.strip() + "." +domain.strip() 
                print(new_domain)
                cert = ssl.get_server_certificate((new_domain, 443))
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
                with open('fingerprints.txt') as fp:
                    for fingerprint in fp:
                        print("Checking fingerprint {fingerprint}".format(fingerprint=fingerprint))
                        fingerprint_stripped = fingerprint.strip()
                        cert_fingerprint = str(x509.digest("sha256")).replace(":","").replace("b\'","").replace("'","")
                        print(cert_fingerprint)
                        if fingerprint_stripped == cert_fingerprint:
                            print("{domain} with fingerprint {fingerprint} match".format(domain=new_domain,fingerprint=fingerprint_stripped))
            except Exception as e:
                print(e)
                