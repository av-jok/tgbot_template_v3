import sys
import nmap
import pynetbox
import ipaddress
import urllib3
import socket

# General vars
netbox_url = 'https://netbox.jok.su/'
netbox_api = '55d1fce82f73c8dd7ec5b188f0eddfd31319a2fb'

# Disable SSL and SSL Warnings
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False


def ip_scan(ip_address):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_address, arguments='-sP -R')
    if len(nm.all_hosts()) != 0:
        return nm[ip_address]['status']['state']
    else:
        return 'down'


def ip_check(ip_address):
    ip_search_status = nb.ipam.ip_addresses.filter(address=ip_address)
    if ip_search_status:
        for item in ip_search_status:
            return item.id, item.display
    return 0, '0.0.0.0/0'


def netbox_remove_ip(ip_id):
    ip_search_result = nb.ipam.ip_addresses.get(id=ip_id)
    if ip_search_result is not None:
        ip_search_result.delete()


def get_dns_by_host(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "unknown-host"


def netbox_add_ip(ip, prefix):
    ip_dns_name = get_dns_by_host(ip)
    ip_add_result = nb.ipam.ip_addresses.create(
        address=f'{ip}/{prefix}',
        dns_name=ip_dns_name
    )
    return ip_add_result


def netb_ipam_update(netbox_ip_id, netbox_ip, prefix, nmap_host_state):
    if (nmap_host_state == 'up') and (netbox_ip_id == 0):
        netbox_add_ip(netbox_ip, prefix)
    elif (nmap_host_state == 'down') and (netbox_ip_id != 0):
        netbox_remove_ip(netbox_ip_id)
    return True


def app_run(subnet):
    ip_list = ipaddress.ip_network(subnet)
    for ip in ip_list:
        last_octet = str(ip).split('.')
        if (int(last_octet[-1]) != 255) and (int(last_octet[-1]) != 0):
            nmap_host_state = ip_scan(str(ip))
            netbox_ip_id, netbox_ip = ip_check(str(ip))
            print(ip, nmap_host_state)
            netb_ipam_update(netbox_ip_id,
                             str(ip),
                             ip_list.prefixlen,
                             nmap_host_state
                             )


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("You not present network, please run: \n -> python netbox_scan.py 192.168.104.0/24")
    else:
        app_run(sys.argv[1])
