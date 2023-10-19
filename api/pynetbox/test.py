# import base64
# import logging
import pynetbox
import urllib3
import re
from trans import transliterate

# from django.core.files.base import ContentFile
# from rest_framework import serializers
# from drf_extra_fields.fields import Base64ImageField

# from pprint import pprint

netbox_url = 'https://netbox.avantel.ru/'
netbox_api = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False

i = 0
devices = nb.dcim.sites.filter(region_id=1)  # asset_tag__ic='авантел', role_id=4, status='offline'
for device in devices:
    print(device, device.slug, transliterate(device.name))
    device.slug = transliterate(device.name)
    # if re.findall(r"(?<!\d)\d{5}(?!\d)", device.asset_tag):
    #     text = re.findall(r"(?<!\d)\d{5}(?!\d)", device.asset_tag)
    #     device.name = device.name.lower()
    #     transliterate = transliterate(device.name)
    #     device.asset_tag = text[0]
    #     device.asset_tag = None
    try:
        # print(device, device.asset_tag, text)
        device.save()
    except pynetbox.RequestError as e:
        print(device.asset_tag, e.error)

    if i == 5:
        exit()
    i += 1

# img = nb.extras.image_attachments.filter(object_id='1')
# print(img.id)

# sites = nb.dcim.sites.filter(status='active', region_id='1')
# for site in sites:
#     site.name = site.name.lower()
#     pprint(dict(site))

# with open("joker.png", "rb") as file_handle:
#     image_data = file_handle.read()
#     base_encoded = base64.b64encode(image_data).decode("utf8")
#     image_data2 = dict(
#         content_type="dcim.device",
#         object_id=8593,
#         name="Test image",
#         image=base_encoded,
#         image_height=512,
#         image_width=512,
#         )
#
#     try:
#         nb.extras.image_attachments.create(image_data2)
#     except pynetbox.RequestError:
#         logging.exception(f"Failed to attach image")
# pprint(dict(image_data))
