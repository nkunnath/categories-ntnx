# Mask Category Permissions
## Introduction

Nutanix does not have RBAC on Categories (at the time of this post). That means project users are able to see all Categories. While this is a FEAT in progress, this script is a workaround to mask the categories view.


## Installation
It is strongly recommended to run this script within a virtual environment and install all of the required dependencies there.

Run in Terminal/Command Prompt:

```
git clone https://github.com/nkunnath/categories-ntnx.git
cd categories-ntnx/
python -m pip install virtualenv
python -m virtualenv venv
```
In UNIX system:
```
source venv/bin/activate
```
In Windows:
```
venv\Scripts\activate
```
To install the required packages to this environment, simply run:
```
pip install -r requirements.txt
```

## Usage

The script connects to a Prism Central instance and masks the permissions required to view Categories.

Run the below from command line.
```
python categories.py -h

usage: 
    There are 3 choices to run the script.
    python categories.py --list_all_roles
    python categories.py --list_roles_with_cat_perm
    python categories.py --delete_cat_permissions <ROLE_UUID>
    

Script to remove category permissions

optional arguments:
  -h, --help            show this help message and exit
  --list_all_roles      List all the roles in the PC
  --list_roles_with_cat_perm
                        List all the roles in the PC which have category permissions
  --delete_cat_permissions DELETE_CAT_PERMISSIONS
                        Delete the view category permissions for one role
```


Look at the screenshots.md for an example.
## License
[MIT](https://choosealicense.com/licenses/mit/)
