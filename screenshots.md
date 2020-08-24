# Screenshots

This is an example.

The Self-service Admin determines that John Legend only needs to be able to view the VM's and resources assigned to him. He should not be able to view all the Categories in the cluster, used in different Projects. 





While the role assigned to John can be edited from the Prism GUI, the specific permissions required here cannot br removed. This is where the script comes in.

 

After running the script, John cannot see any Categories. 



## Caveats
1) This script masks all the Categories, ie, it is not possible to view only some Categories for some users.
1) It is possible to revert this behaviour. If the permission list for the role is changed to include more permissions or Full Access to VM is assigned to the role, the Category permissions will be re-added. The script can be run as necessary.

