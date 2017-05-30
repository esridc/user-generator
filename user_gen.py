from arcgis.gis import GIS
import os
import argparse
import csv
import random

# uncomment the environment you want to create users in

# DEV
# ENV = "https://devext.arcgis.com"
# gis = GIS(url=ENV, username=os.environ['COMM_ORG_USER_DEV'], password=os.environ['COMM_ORG_PWORD_DEV'])

# # QA
ENV = "https://qaext.arcgis.com"
gis = GIS(url=ENV, username=os.environ['COMM_ORG_USER_QA'], password=os.environ['COMM_ORG_PWORD_QA'])

# PROD
# ENV = "https://flying5123.maps.arcgis.com"
# gis = GIS(url=ENV, username=os.environ['COMM_ORG_USER_PROD'], password=os.environ['COMM_ORG_PWORD_PROD'])


def destroy_user(username):
    username = gis.users.get(username)
    deleted = username.delete()
    return deleted


def create_username(fname, lname):
    username = fname + lname + '_qa_mock_acct'

    if gis.users.get(username):
        username = fname + lname + '_qa_mock_acct' + str(random.randint(999, 9999))
    else:
        pass
    return username


def create_dummy_group():
    try:
        group = gis.groups.search('QA_dummyUser')[0]
    except:
        group = gis.groups.create(title='QA_dummyUser',
                                  tags='QA_dummyUser',
                                  description=None,
                                  snippet=None,
                                  access='public'
                                  )
    return group


def destroy_dummy_group_members(num_to_destroy):
    count = 0
    try:
        myGroup = gis.groups.search('QA_dummyUser')[0]
        myGroup = myGroup.get_members()['users']
        if num_to_destroy != 'all':
            holding_group = [myGroup[i] for i in range(0, num_to_destroy)]
        if num_to_destroy == 'all':
            holding_group = myGroup
        for member in holding_group:
            if member[-13:] == '_qa_mock_acct' or member[-18:-4] == '_qa_mock_acct':
                x = gis.users.get(member)
                x.delete()
                print('{}. {} destroyed'.format(count + 1, member))
                count += 1
    except Exception as e:
        print(e)
    return


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--count", type=int, help="the number of users you want to generate")
parser.add_argument("-d", "--destroy", type=str, help="destroy the previously created group")
args = parser.parse_args()

if args.count:
    with open('fake_users.csv', newline='') as csvFile:
        nameReader = csv.reader(csvFile, delimiter=',')
        nameReader = [name for name in nameReader]
        random.shuffle(nameReader)  # commment out this line to generate users as they appear in the csv
        count = 0
        listOfUsernames = []
        listOfFakeEmailHosts = ['@tmail.com', '@bahoo.com', '@coldmail.com', '@inlook.com', '@footbook.com']

        for item in nameReader:
            dummy_username = create_username(item[0], item[1])
            dummy_email = '{}{}'.format(dummy_username.rstrip('_qa_mock_acct'), random.choice(listOfFakeEmailHosts))

            try:
                new_dummy = gis.users.create(username=dummy_username,
                                             password='qamockacct1',
                                             firstname=item[0],
                                             lastname=item[1],
                                             email=dummy_email,
                                             description='test account created using a script for QA purposes',
                                             role='org_user',
                                             provider='arcgis',
                                             level=2
                                             )
            except:
                pass

            listOfUsernames.append(new_dummy.username)
            print('{}. Created {}'.format(count + 1, new_dummy.username))
            count += 1
            if count == args.count:
                break

    g = create_dummy_group()
    g.add_users(listOfUsernames)

if args.destroy:
    try:
        t = int(args.destroy)
        destroy_dummy_group_members(t)
    except:
        t = 'all'
        destroy_dummy_group_members(t)
