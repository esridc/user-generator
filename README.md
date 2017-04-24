# User Generator
This is a script that allows for rapid creation and deletion of ArcGIS user accounts in a specified organization.
It requires the ArcGIS Python API to achieve this. 


# Required to run:
* [ArcGIS Python API](https://developers.arcgis.com/python/)
* An ArcGIS organization 
* An account with admin permissions in said organization
* CSV of fake user names


# How it works: 
Included with the script is a csv of 500 computer generated names. The script uses this CSV to create users by concatenating the first and last names and appending `_QAdummy`  to the end of it. It uses this as the base for the username. It checks that an account doesn't already exist with that username in the organization. In the event a user account with that names does exist, the script will generate a 4 digit number and append that to the end of the username.

All users created via thia script are added to a a group named `QA_dummyUser`, which is used when it's necessary to destroy script-generated users, be that all of them or just a subset of them.

### command line input accepted:
* `-c <number>`  create users: number is between 1-500
* `-d <number>`  destroy users: number is between 1 and amount of users in the dummy group
* `-d all`       destroy all users

### examples:
* `python3 user_gen.py -c 5`

Would generate 5 users in the specified organization

* `python3 user_gen.py -d 2`

Would destroy 2 of those generated users.

* `python3 user_gen.py -d all`

Would destroy all other previously script-generated users