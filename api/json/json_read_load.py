import json

with open('sw_templates.json') as f:
    templates = json.load(f)

print(templates)

for section, commands in templates.items():
    print(section)
    print('\n'.join(commands))

with open('sw_templates.json') as f:
    file_content = f.read()
    templates = json.loads(file_content)


for section, commands in templates.items():
    print(section)
    print('\n'.join(commands))


trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk native vlan 999', 'switchport trunk allowed vlan'
]

access_template = [
    'switchport mode access', 'switchport access vlan',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

to_json = {'trunk': trunk_template, 'access': access_template}

with open('sw_templates2.json', 'w') as f:
    f.write(json.dumps(to_json))

with open('sw_templates2.json') as f:
    print(f.read())


with open('sw_templates3.json', 'w') as f:
    json.dump(to_json, f, sort_keys=True, indent=2)

with open('sw_templates3.json') as f:
    print(f.read())
