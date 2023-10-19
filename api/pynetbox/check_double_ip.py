import pynetbox

URL = 'https://netbox.avantel.ru/'
API_TOKEN = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
nb = pynetbox.api(url=URL, token=API_TOKEN, threading=True)

print('Getting IP addresses...')
# get all ip
ipaddr_all = nb.ipam.ip_addresses.all()

# set to list
addr_list = []
for address in ipaddr_all:
    addr_list.append(str(address))
print('Count', len(addr_list), 'IP addresses, finding duplicates...')

# Finding duplicates
addr_list_nodup = []
addr_list_dup = []
for address in addr_list:
    if address not in addr_list_nodup:
        addr_list_nodup.append(address)
    else:
        addr_list_dup.append(address)

if len(addr_list_dup) > 0:
    for address in addr_list_dup:
        print('Found duplicate IP:', address)
else:
    print('No duplicates found')
