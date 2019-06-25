# curl https://phabricator.services.mozilla.com/api/differential.revision.search \
#     -d api.token=api-token \
#     -d constraints[ids][0]=27870

import json
import os

import dotenv
import requests

CONF = dotenv.find_dotenv()
if CONF:
    dotenv.load_dotenv(CONF)


def _conduit_request(api_url, data):
    api_url = f"{os.getenv('CONDUIT_API_URL')}/{api_url}"
    data['api.token'] = os.getenv('CONDUIT_API_KEY_1')

    s = requests.Session()
    req = requests.Request('POST', api_url, data=data)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    resp.raise_for_status()
    results = resp.json()
    return results['result']['data']


def get_conduit_revision(constraints):
    payload = {'constraints[ids][]': constraints}
    return _conduit_request('differential.revision.search', payload)

    # data = {
    #     'api.token': os.getenv('CONDUIT_API_KEY_1'),
    #     'constraints[ids][]': constraints
    # }

    # s = requests.Session()
    # api_url = os.getenv("CONDUIT_API_URL") + "/differential.revision.search"
    # req = requests.Request('POST', api_url, data=data)
    # prepped = s.prepare_request(req)
    # resp = s.send(prepped)
    # resp.raise_for_status()
    # results = resp.json()
    # return results["result"]["data"]


def is_public_revision(revision):
    return revision["fields"]["policy"]["view"] == "public"


response = get_conduit_revision(27870)
print(json.dumps(response, indent=2))

# print(json.dumps(response, indent=2, sort_keys=False))
# print("public?", is_public_revision(response))
