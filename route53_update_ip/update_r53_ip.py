import boto3, json, argparse
from get_public_ip import get_public_ip

def update_ip_address(client, domain, ip):
    response = client.list_hosted_zones_by_name(
    DNSName=domain, 
    MaxItems='1'
    )
    # print(json.dumps(response, indent=4)) # inspect output
    if ('HostedZones' in response.keys()
        and len(response['HostedZones']) > 0
        and response['HostedZones'][0]['Name'].startswith(domain)):
        hosted_zone_id = response['HostedZones'][0]['Id'].split('/')[2] # response comes back with /hostedzone/{HostedZoneId}
        print('HostedZone {} found with Id {}'.format(domain, hosted_zone_id))
    else:
        print('HostedZone not found: {}'.format(domain))


    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": domain,
                        "Type": "A",
                        "TTL": 180,
                        "ResourceRecords": [
                            {
                                "Value": ip
                            },
                        ],
                    }
                },
            ]
        }
    )    


def main():
    parser = argparse.ArgumentParser(description='A python script used to update the IP of the hosted zone')
    parser.add_argument('-d','--domain', help='The domains IP to check to ensure IP resolves properly for certbot', required=True)
    args = vars(parser.parse_args())
    session = boto3.session.Session()

    client = session.client('route53')
    domain = args['domain']
    ip = get_public_ip()
    update_ip_address(client, domain, ip)

if __name__ == "__main__":
    main()