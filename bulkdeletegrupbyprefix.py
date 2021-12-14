#!/usr/local/opt/python@3.8/bin/python3.8
# coding: utf-8
import urllib.parse
import urllib3
import ssl
import json
import requests

# Create auto-login for NSX
ssl._create_default_https_context = ssl._create_unverified_context
s = requests.Session()
s.verify = False
s.auth = ('<USERNAME>', '<PASSWORD>')
nsx_mgr = 'https://<NSX-T MGR FQDN>'
urllib3.disable_warnings()

#Retrieve list of groups
nsgroups_upath = '/policy/api/v1/infra/domains/default/groups' 
data = s.get(nsx_mgr + nsgroups_upath).json()
nsgroups = data["result_count"]

#Add group name to new list
group_name_list = []
for i in range(nsgroups):
    group_name_list.append(data["results"][i]["id"])

#Match Groups to be deleted
for i in group_name_list:
    a = str(i[:8]) # <- Match on the first 8 characters (prefix) of the group name
    if a == 'My_Group': # <- If first 8 characters equal the string 'My_Group' delete the group
        group_name = (str(i))
        group_delete_upath = '/policy/api/v1/infra/domains/default/groups/' + group_name 
        s.delete(nsx_mgr + group_delete_upath, headers=s.headers, auth=s.auth, verify=s.verify)
