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


def get_conduit_revision(id):
    data = {
      "api.token": os.getenv("CONDUIT_API_KEY_1"),
      "constraints[ids][0]": id
    }
    api_url = os.getenv("CONDUIT_API_URL") + "/differential.revision.search"
    res = requests.post(api_url, data=data).json()
    return res["result"]["data"][0]


def is_public_revision(revision):
    return revision["fields"]["policy"]["view"] == "public"


response = get_conduit_revision(27870)

print(json.dumps(response, indent=2, sort_keys=False))
print("public?", is_public_revision(response))
