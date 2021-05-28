from flask import Flask, render_template
from flask_restful import Resource, Api, abort
import functools

from dns_restful.aliyundns.aliyundns import AliyunDNS

app = Flask(__name__)
api = Api(app)
client = AliyunDNS(None, None, None, None)
envs = dict()


def init(e):
    global client, envs
    envs = e
    client = AliyunDNS(envs['access_key_id'], envs['access_secret'], envs['domain'], envs['region_id'])


def check_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs['token'] is None:
            return abort(404, message='token not found')
        if kwargs['token'] != envs['token']:
            return abort(404, message=f'invalid token: {kwargs["token"]}')
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


class ListDomainRecords(Resource):
    @check_token
    def get(self, token):
        return {'status': 'ok', 'token': token,
                'records': [{'subdomain': r['RR'], 'value': r['Value']} for r in client.list()]}


class SetDomainRecord(Resource):
    @check_token
    def get(self, subdomain, value, token):
        if client.get(subdomain) is not None:
            client.update(subdomain, value)
        else:
            client.add(subdomain, value)
        return {'status': 'ok', 'token': token}


class GetDomainRecord(Resource):
    @check_token
    def get(self, subdomain, token):
        return {'status': 'ok', 'token': token, 'subdomain': subdomain, 'value': client.get(subdomain)}


class DeleteDomainRecord(Resource):
    @check_token
    def get(self, subdomain, token):
        client.delete(subdomain)
        return {'status': 'ok', 'token': token}


api.add_resource(ListDomainRecords, '/list/<token>')
api.add_resource(SetDomainRecord, '/set/<subdomain>/<value>/<token>')
api.add_resource(GetDomainRecord, '/get/<subdomain>/<token>')
api.add_resource(DeleteDomainRecord, '/delete/<subdomain>/<token>')


class Metrics(Resource):
    def get(self):
        return {
            'status': 'ok',
        }


api.add_resource(Metrics, '/metrics')
