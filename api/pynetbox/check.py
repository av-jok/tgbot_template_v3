import pynetbox
import datetime
import markdown

# nb = pynetbox.api(
#     'http://omicron.lan.uctrl.net:8001',
#     token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# )

URL = 'https://netbox.avantel.ru/'
API_TOKEN = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
nb = pynetbox.api(url=URL, token=API_TOKEN, threading=True)


entries = nb.extras.journal_entries.filter(assigned_object_type="dcim.rack", assigned_object_id=481)

for entry in entries:
    date = datetime.datetime.fromisoformat(entry.created.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    html = markdown.markdown(entry.comments).replace("\n", "")

    print(f'{entry.kind.value}|<p class="timestamp">{date}</p>{html}')
