import json
import sys
import argparse
import getpass
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def make_request(ip_address,user):
    '''
    Function that return the response of the REST API call to list all the roles
    '''
    header = {"content-type": "application/json"}
    data_list = {
      "kind": "role",
      "length": 500,
      "offset": 0
    }
    auth = HTTPBasicAuth(user, getpass.getpass('Enter the password: '))
    url_list = "https://{0}:9440/api/nutanix/v3/roles/list".format(ip_address)
    res_list = requests.post(url=url_list, data=json.dumps(data_list), auth=auth, headers=header, verify=False)
    return res_list


def list_all_roles(ip_address,username):
    '''
    List all the roles
    '''
    res_list = make_request(ip_address,username)
    role_list = []
    for role in res_list.json().get('entities'):
        tup = (role.get('status').get('name'), role.get('metadata').get('uuid'))
        role_list.append(tup)
    print("All the roles in this cluster are")
    for role in role_list:
        print(role)


def list_roles_with_cat_perm(ip_address, username):
    '''
    List all the roles that have view category permissions
    '''
    res_list = make_request(ip_address, username)
    role_list = []
    for role in res_list.json().get('entities'):
        permission_list = role.get('status').get('resources').get('permission_reference_list')
        for permission in permission_list:
            if permission.get('name') == "View_Name_Category":
                tup = (role.get('status').get('name'), role.get('metadata').get('uuid'))
                role_list.append(tup)
    print('The roles with category permissions and their corresponding UUID are')
    for role in role_list:
        print(role)
    return role_list


def delete_cat_permissions(ip_address, username, uuid):
    '''
    Delete view category permissions from one role.
    The function creates a new body without the two permissions - View_Name_Category and View_Value_Category
    and sends the updated request
    '''
    url_get = "https://{0}:9440/api/nutanix/v3/roles/{1}".format(ip_address, uuid)
    auth = HTTPBasicAuth(username, getpass.getpass('Enter the password: '))
    res_get = requests.get(url=url_get, auth=auth, verify=False)
    placeholder_list = []
    permission_list_status = res_get.json().get('status').get('resources').get('permission_reference_list')
    permission_list_spec = res_get.json().get('spec').get('resources').get('permission_reference_list')
    print("This role has", len(permission_list_spec), "permissions now")

    for permission in permission_list_status:
        if permission.get('name') == "View_Name_Category":
            placeholder_list.append(permission.get('uuid'))
        if permission.get('name') == "View_Value_Category":
            placeholder_list.append(permission.get('uuid'))

    #Create new permission list
    new_perm_ref_list = [] 
    for permission in permission_list_spec:
        if len(placeholder_list) == 0:
            print("View_Name_Category and View_Value_Category not found in list of permissions")
            break
        if permission.get('uuid') not in placeholder_list:
            new_perm_ref_list.append(permission)
    print('Number of permissions after running the script will be', len(new_perm_ref_list))

    #Create new metadata
    list_meta_dict = ['kind', 'uuid', 'spec_version', 'categories_mapping', 'owner_reference', 'categories']
    new_metadata = {key : res_get.json().get('metadata')[key] for key in list_meta_dict}

    #Create new payload 
    new_payload = {"api_version" : res_get.json().get('api_version'),
                  "metadata" : new_metadata,
                  "spec" : {
                      "name" : res_get.json().get('spec').get('name'),
                      "resources": {
                        "permission_reference_list" : new_perm_ref_list
                      }
                  }
    }
    header = {"content-type": "application/json"}

    if placeholder_list:
        print('The permissions to be removed are {}'.format(placeholder_list))
        print('Sending request to delete the two category permissions')
        res_post = requests.put(url=url_get, data=json.dumps(new_payload), verify=False, auth=auth, headers=header)
        print(res_post.status_code)


def get_pc_info():
    ip_address = str(input('Enter Prism Central IP address: '))
    username = str(input('Enter username: '))
    return ip_address,username


def main():
    parser = argparse.ArgumentParser(description='Script to remove category permissions', 
                                     usage='''
    There are 3 choices to run the script.
    python categories.py --list_all_roles
    python categories.py --list_roles_with_cat_perm
    python categories.py --delete_cat_permissions <ROLE_UUID>
    ''')
    parser.add_argument('--list_all_roles', help='List all the roles in the PC', action="store_true")
    parser.add_argument('--list_roles_with_cat_perm', help='List all the roles in the PC which have category permissions', 
                        action="store_true")
    parser.add_argument('--delete_cat_permissions', type=str, help='Delete the view category permissions for one role')
    args = parser.parse_args()
    
    if len(sys.argv) == 2:
        ip_address, username = get_pc_info()
        if args.list_all_roles:
            list_all_roles(ip_address,username)
        if args.list_roles_with_cat_perm:
            list_roles_with_cat_perm(ip_address,username)
    elif len(sys.argv) == 3:
        if args.delete_cat_permissions:         
            ip_address, username = get_pc_info()
            delete_cat_permissions(ip_address, username, args.delete_cat_permissions)
    else:
        print("Incorrect number of arguments. Please run python categories.py -h")
        

if __name__ == "__main__":
    main()

