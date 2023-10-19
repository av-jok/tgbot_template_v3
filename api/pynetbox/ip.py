import pynetbox
import urllib3


# General vars
netbox_url = 'https://netbox.jok.su/'
netbox_api = '55d1fce82f73c8dd7ec5b188f0eddfd31319a2fb'

# Disable SSL and SSL Warnings
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False

dev_type = nb.dcim.device_types.get(slug="3750g-48ts")
dev_role = nb.dcim.device_roles.get(slug="management-switch")
dev_site = nb.dcim.sites.get(slug="kampala-dc-01")

ip_search = nb.ipam.ip_addresses.filter(address='10.0.96.2')
print(ip_search)
