import json
import pynetbox
import ipaddress
import urllib3
import logging

logging.basicConfig(level=logging.INFO)

# General vars
# netbox_url = 'https://netbox.jok.su/'
netbox_url = 'https://netbox.avantel.ru/'

netbox_api = '55d1fce82f73c8dd7ec5b188f0eddfd31319a2fb'

# Disable SSL and SSL Warnings
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False


def netbox_add_ip(ip, prefix=22):
    ip_add_result = nb.ipam.ip_addresses.create(
        address=f'{ip}/{prefix}',
    )
    return ip_add_result


def ip_check(address):
    ip_search_status = nb.ipam.ip_addresses.filter(address=address)
    if ip_search_status:
        for item in ip_search_status:
            return item.id
    return False


dev_type = nb.dcim.device_types.get(slug="template")
dev_role = nb.dcim.device_roles.get(slug="access-switch")
dev_site = nb.dcim.sites.get(slug="unilink")


with open('zbx_export_hosts.json') as file:
    zbx_dict = json.load(file)

for host in zbx_dict['zabbix_export']['hosts']:
    try:
        ipv4 = ipaddress.ip_address(host['host'])
    except ValueError:
        logging.debug(f"{host['host']} пропускаем")

        continue

    if not ipaddress.IPv4Address(ipv4) in ipaddress.IPv4Network('10.0.0.0/8'):
        logging.debug(f"{ipv4} не подходящий IP, пропускаем")
        continue

    if nb.dcim.devices.get(name=host['name']) is None:

        # print(host['name'].lower())

        dev_dict = dict(
            name=host['name'].lower(),
            device_type=dev_type.id,
            role=dev_role.id,
            device_role=dev_role.id,
            site=dev_site.id,
            status="offline",
        )

        # Add device to NetBox and store resulting object in "new_dev"
        new_dev = nb.dcim.devices.create(dev_dict)

        intf_dict = dict(
            name="Vlan1000",
            form_factor=0,
            type="virtual",
            description="Management SVI",
            device=new_dev["id"]
        )

        # Add interface to NetBox and store resulting object in "new_intf"
        new_intf = nb.dcim.interfaces.create(intf_dict)

        # Prepare dict with attributes for Management IP address
        ip_add_dict = dict(
            address=f"{ipv4}/22",
            status="active",
            description="Management IP for {}".format(dev_dict["name"]),
            interface=new_intf["id"],
            assigned_object_type="dcim.interface",
            assigned_object_id=new_intf["id"]
        )

        # Add interface to NetBox and store resulting object in "new_ip"
        new_ip = nb.ipam.ip_addresses.create(ip_add_dict)

        new_dev.primary_ip = new_ip
        new_dev.primary_ip4 = new_ip

        new_dev.save()
        # Display summary, just to see if objects were really created
        logging.info("Device '{dev}' created with interface '{intf}', which has IP {ipadd}.".format(dev=new_dev["name"], intf=new_intf["name"], ipadd=new_ip["address"]))
    else:
        logging.debug(f"{host['host'].lower()} существует, пропускаем")

