#!/usr/bin/python

# Copyright: (c) 2018, Itential <opensource@itential.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: iap_get_workflow_job_variables
version_added: "2.6"
author: "Itential (opensource@itential.com)"
short_description: Get job variables of a workflow from the Itential Automation Platform
description:
  - This will get the job variables of a workflow from the Itential Automation Platform.
options:
  iap_port: 
    description: 
      - Provide the port number for the Itential Automation Platform  
    required: true
    default: null

  iap_fqdn: 
    description: 
      - Provide the fqdn for the Itential Automation Platform  
    required: true
    default: null
    
  workflow_name: 
    description: 
      - Provide the workflow name 
    required: true
    default: null
  
  https: 
    description: 
      - The transport protocol is HyperText Transfer Protocol Secure (HTTPS) for the Itential Automation Platform 
      - By default using http
    type: bool
    default: False
    
requirements:
  - the Itential Automation Platform with relevant applications

notes:
  - This module is under construction

'''

EXAMPLES = '''
- name: Get job variables of workflow from the Itential Automation Platform
      iap_get_workflow_job_variables:
        iap_port: 3000
        iap_fqdn: localhost
        token_key: "DFSFSFHFGFGF[DSFSFAADAFASD%3D"
        workflow_name: "RouterUpgradeWorkflow"
      register: result

    - debug: var=result.response
'''

RETURN = '''
response:
    description: The result contains the response from the call
    type: object
'''

# Ansible imports
from ansible.module_utils.basic import *

# Standard library imports
import requests


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        iap_port=dict(type='str', required=True),
        iap_fqdn=dict(type='str', required=True),
        token_key=dict(type='str', required=True),
        workflow_name=dict(type='str', required=True),
        https=(dict(type='bool', default=False))
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        response=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed
    # hit the target system and get the job variables of workflow
    # defaulting the value for transport_protocol to be : http
    transport_protocol = 'http'
    if module.params['https'] is True:
        transport_protocol = 'https'

    application_token = module.params['token_key']
    url = transport_protocol+"://"+module.params['iap_fqdn'] + ":" +module.params['iap_port']+"/workflow_engine/workflows/variables/"+\
          module.params['workflow_name']+"?token=" + str(application_token)

    try:
        r = requests.get(url=url, headers={"content-type": "application/json"})
        r.raise_for_status()
        if r.status_code == 200:
            result['changed'] = True
            result['response'] = r.json()
    except requests.ConnectionError as err:
        module.fail_json(msg="Failed to connect to Itential Automation Platform : {} ".format(err), **result)
    except requests.exceptions.HTTPError as errh:
        module.fail_json(msg="Http Error: {} ".format(errh), **result)
    except requests.exceptions.Timeout as errt:
        module.fail_json(msg="Timeout Error: {} ".format(errt), **result)
    except requests.exceptions.RequestException as err:
        module.fail_json(msg="Something happened: {} ".format(err), **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()