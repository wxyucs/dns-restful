# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

import json
import logging


class AliyunDNS:
    def __init__(self, access_key_id, access_secret, domain, region_id):
        self.client = AcsClient(f'{access_key_id}', f'{access_secret}', region_id)
        self.domain = domain

    def list(self):
        """
        List all domain record, contains 'RR', 'Value', 'RecordId'.
        """
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(f'{self.domain}')
        response = str(self.client.do_action_with_exception(request), encoding='utf-8')
        origin = json.loads(response)
        logging.debug(origin)
        return [{'RR': record['RR'], 'Value': record['Value'], 'RecordId': record['RecordId']}
                for record in origin['DomainRecords']['Record']]

    def get(self, rr):
        """
        Get dns record of specify domain. Return None if record not exists.

        :param rr: subdomain
        """
        for r in self.list():
            if r['RR'] == rr:
                return r['Value']
        return None

    def add(self, rr, value):
        """
        Add a new domain record, failed if rr existed.

        :param rr: subdomain
        :param value: ip address
        """
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        request.set_DomainName(f'{self.domain}')
        request.set_RR(f'{rr}')
        request.set_Type(f'A')
        request.set_Value(f'{value}')
        response = str(self.client.do_action_with_exception(request), encoding='utf-8')
        logging.debug(json.loads(response))

    def delete(self, rr):
        """
        Delete specify domain record if exists.

        :param rr: subdomain
        """
        record_id = None
        records = self.list()
        for record in records:
            if record['RR'] == rr:
                record_id = record['RecordId']
                break
        if record_id is None:
            logging.debug(f'AliyunDNS::delete: record for {rr + "." + self.domain} does not exist, ignore')
            return
        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(f'{record_id}')
        response = str(self.client.do_action_with_exception(request), encoding='utf-8')
        logging.debug(json.loads(response))

    def update(self, rr, value):
        """
        Update the record for specify subdomain.

        :param rr: subdomain
        :param value: ip address
        """
        recordid = str()
        records = self.list()
        for record in records:
            if record['RR'] == rr:
                recordid = record['RecordId']
        if recordid == '':
            logging.debug(f'AliyunDNS::update: record for {rr + "." + self.domain} does not exist, ignore')
            return
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(f'{recordid}')
        request.set_RR(f'{rr}')
        request.set_Type(f'A')
        request.set_Value(f'{value}')
        response = str(self.client.do_action_with_exception(request), encoding='utf-8')
        logging.debug(json.loads(response))
