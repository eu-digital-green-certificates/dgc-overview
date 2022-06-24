# ---license-start
# cmsmig.py - CMS migration tool
# ---
# Copyright (C) 2022 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end
#
# Requirements: requests asn1crypto cryptography
# Usage: python3 cmsmig.py --help

baseurls = {
    'TST': 'https://test-dgcg-ws.tech.ec.europa.eu',
    'ACC': 'https://acc-dgcg-ws.tech.ec.europa.eu',
}
cert_folder = 'certificates'
# cert folder is supposed to contain: 
#  - auth.pem + key_auth.pem        (TLS/Auth certificate + key)
#  - upload.pem + key_upload.pem    (UPLOAD certificate + key)

import json
import requests
from os import path
from asn1crypto import cms
from hashlib import sha256
from cryptography import x509
from argparse import ArgumentParser
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import hashes, serialization

def main(args):
    if not args.environment.upper() in baseurls: 
        print(f'Unknown environment: {args.environment.upper()}')
        return

    if args.command.lower() == 'list':
        list_migratables(args)
    elif args.command.lower() == 'migrate': 
        migrate(args)


def migrate(args):
    if args.entities is None or len(args.entities) == 0: 
        print('Specify which entities to migrate')
        return False

    print('Getting list of migratables from gateway')
    migratables = get_migratables(args)
    migratables_by_eId = { str(e['entityId']) : e for e in migratables }
    eIds = [ e.upper() for e in args.entities ]
    
    if len(eIds) == 1 and eIds == ['ALL']:
        print('Migrating all entities')
        response = input('Are you sure (only "yes" as answer will execute)? ')
        if not response.upper() == 'YES':
            print('Aborting')
            return False
        eIds = migratables_by_eId.keys()

    for eId in eIds: 
        if not eId in migratables_by_eId: 
            print(f'Error: unknown entity ID: {eId}')
        else:
            payload = get_payload(migratables_by_eId.get(eId))
            new_entry = migratables_by_eId.get(eId).copy()
            new_entry['cms'] = str(create_cms(args, payload), 'utf-8')
            response = requests.post(baseurls[args.environment.upper()] + "/cms-migration", cert=get_auth(args), json=new_entry )
            print(f'Migration of eID {eId} returned status {response.status_code}')
    

def list_migratables(args): 
    'Print a table of the migratable entities'

    print('Getting list of migratables from gateway')
    migratables = get_migratables(args)
    print('{:<12}{:<20}{:<20}'.format('entity ID', 'type', 'info'))
    print('------------------------------------------------------------')
    for entry in migratables: 
        if entry.get('cms') is not None:
            payload = get_payload(entry) 
            if entry['type'] == 'VALIDATION_RULE':
                jpayload = json.loads(payload)
                extra_info = f'Rule-ID: {jpayload["Identifier"]} {jpayload["Version"]}'
            elif entry['type'] == 'REVOCATION_LIST':
                jpayload = json.loads(payload)
                extra_info = f'KID: {jpayload["kid"]}, hashcount: {len(jpayload["entries"])}'
            elif entry['type'] == 'DSC':
                kid = str(b64encode(sha256(payload).digest()[:8]),'utf-8')
                extra_info = f'KID: {kid}'
            else:
                extra_info = ''

            print(f'{entry["entityId"]:>8}    {entry["type"]:<20}  {extra_info}')


def create_cms(args, data):
    ''' Create a CMS of the data (bytes) using the upload cert+key of the country from args.
        Result is base64 encoded'''
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(cert_folder, 'upload.pem'), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(cert_folder, 'key_upload.pem'), "rb").read(), None)

    options = [serialization.pkcs7.PKCS7Options.Binary]

    builder = serialization.pkcs7.PKCS7SignatureBuilder().set_data(data)
    signed = builder.add_signer(upload_cert, upload_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    return b64encode(signed)



def get_payload(entry):
    'Decode the CMS payload of an entry from the list of migratables'

    cInfo = cms.ContentInfo.load(b64decode(entry['cms']))
    
    payload = dict(dict(dict(cInfo.native)['content'])['encap_content_info'])['content']    

    return payload

def get_signature(entry, signer_no=0):
    '''Get the signature of an entry. In case there are multiple signers, the signer_no can be set. 
       This should never happen in DCC context though.'''

    cInfo = cms.ContentInfo.load(b64decode(entry['cms']))

    try:
        return dict(dict(cInfo.native)['content'])['signer_infos'][signer_no]['signature']        
    except IndexError:
        return None


def get_migratables(args):
    'Get the list of migratables in JSON formt from the gateway'

    response = requests.get(baseurls[args.environment.upper()] + "/cms-migration", cert=get_auth(args) )
    assert response.ok, f'Failed to get list of migratables: HTTP {response.status_code} {response.text}'

    if args.type is None: 
        return response.json()
    else:
        return [ entry for entry in response.json() if entry['type'] == type_name(args.type) ]

def get_auth(args):    
    auth = path.join(cert_folder, 'auth.pem')
    key_auth = path.join(cert_folder, 'key_auth.pem')
    return (auth, key_auth)


def type_name(type_str):
    '''Return the correct type name, so for example
            REVOCATION --> REVOCATION_LIST
            RevocationList --> REVOCATION_LIST
            rule --> VALIDATION_RULE
            etc.
    '''
    type_str = type_str.strip().upper()
    if type_str in ['DSC','CERT','CERTIFICATE']:
        return 'DSC'
    elif type_str.startswith('REVO'):
        return 'REVOCATION_LIST'
    elif type_str.endswith('RULE'): 
        return 'VALIDATION_RULE'
    else:
        return None

if __name__ == "__main__":
    parser = ArgumentParser(description='Manage CMS migrations')
    parser.add_argument('-e','--environment', default='TST', help='Environment: TST or ACC')
    parser.add_argument('command', help='Commands: list, migrate')
    parser.add_argument('entities', nargs='*', help='Entity IDs for migrate command (or "all")')
    parser.add_argument('-t', '--type', required=False, help='type of migratable (DSC, REVOCATION or RULE)')
    args = parser.parse_args()
    main(args)