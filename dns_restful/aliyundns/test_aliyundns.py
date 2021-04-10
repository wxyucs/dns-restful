import unittest
import logging
import random
import os
from .aliyundns import AliyunDNS
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
access_key_id = os.getenv('ACCESS_KEY_ID')
access_secret = os.getenv('ACCESS_SECRET')
domain = os.getenv('DOMAIN')
region_id = os.getenv('REGION_ID')
assert None not in (access_key_id, access_secret, domain, region_id)


class DNSTableCase(unittest.TestCase):
    RESERVE_DOMAIN = 'admin'
    RESERVE_RECORD = '127.0.0.1'

    def test_list(self):
        dns = AliyunDNS(access_key_id, access_secret, domain, region_id)
        records = dns.list()
        logging.debug(records)
        self.assertEqual(type(records), list)
        for record in records:
            if record['RR'] == DNSTableCase.RESERVE_DOMAIN:
                self.assertEqual(record['Value'], DNSTableCase.RESERVE_RECORD)
                return
        # admin not found in records
        self.assertEqual(True, False)

    def test_get(self):
        dns = AliyunDNS(access_key_id, access_secret, domain, region_id)
        record = dns.get(DNSTableCase.RESERVE_DOMAIN)
        self.assertEqual(record, DNSTableCase.RESERVE_RECORD)

    def test_add_and_delete(self):
        dns = AliyunDNS(access_key_id, access_secret, domain, region_id)
        while True:
            subdomain = 'ut' + str(random.randint(100000, 999999))
            if dns.get(subdomain) is None:
                break
        dns.add(subdomain, '8.8.8.8')
        self.assertEqual(dns.get(subdomain), '8.8.8.8')
        dns.delete(subdomain)
        self.assertEqual(dns.get(subdomain), None)

    def test_add_update_and_delete(self):
        dns = AliyunDNS(access_key_id, access_secret, domain, region_id)
        while True:
            subdomain = 'ut' + str(random.randint(100000, 999999))
            if dns.get(subdomain) is None:
                break
        dns.add(subdomain, '8.8.8.8')
        self.assertEqual(dns.get(subdomain), '8.8.8.8')
        dns.update(subdomain, '4.4.4.4')
        self.assertEqual(dns.get(subdomain), '4.4.4.4')
        dns.delete(subdomain)
        self.assertEqual(dns.get(subdomain), None)


if __name__ == '__main__':
    unittest.main()
