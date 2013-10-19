import requests
import json
import pprint


url = "https://www.govtrack.us/api/v2/"
beginning = "2013-10-1"
end = "2013-12-31"

def get_mocs():
    payload = {'current': 'true', 'limit': '600'} #enough for all mocs

    r = requests.get(url + "role", params=payload)
    roles = r.json()

    sens = []
    reps = []

    for role in roles['objects']:
        if role['role_type'] == 'senator':
            sens.append(role['person']['id'])
        elif role['role_type'] == 'representative':
            reps.append(role['person']['id'])

    return sens, reps


def get_sponsored_bills(member_id):
    payload = {'sponsor': member_id, 'introduced_date__gte': beginning, 'introduced_date__lte': end}
    
    r = requests.get(url + "bill", params=payload)
    bills = r.json()

    sponsoredBills = [bill['id'] for bill in bills['objects']]

    return sponsoredBills

sens, reps = get_mocs()
sponsorships = {}

#get list of bills sponsored.
for moc in sens + reps:
    sponsorships[moc] = get_sponsored_bills(moc)



print sponsorships.values()
print "total of " + str(sum([len(x) for x in sponsorships.values()]))
