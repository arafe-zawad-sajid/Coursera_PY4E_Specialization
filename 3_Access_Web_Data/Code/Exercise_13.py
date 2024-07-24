# using xml
import xml.etree.ElementTree as ET

data = '''
<person>
    <name>Chuck</name>
    <phone type="intl">+1 734 303 4456</phone>
    <email hide="yes"/>
</person>'''

tree = ET.fromstring(data)
print(tree.find('name').text)
print(tree.find('phone').text)
print(tree.find('email').get('hide'))
print()

input = '''
<stuff>
    <users>
        <user x="2">
            <id>001</id>
            <name>Chuck</name>
        </user>
        <user x="7">
            <id>009</id>
            <name>Brent</name>
        </user>
    </users>
</stuff>'''

stuff = ET.fromstring(input)
user_tags = stuff.findall('users/user')
print(len(user_tags), '\n')

for user_tag in user_tags:
    print(user_tag.get('x'))
    print(user_tag.find('id').text)
    print(user_tag.find('name').text)
print()
# -------------------------------------

# using json
import json

data = '''
{
    "name" : "Chuck",
    "phone" : {
        "type" : "intl",
        "number" : "+1 734 303 4456"
    },
    "email" : {
        "hide" : "yes"
    }
}'''

info = json.loads(data)
print(info)
for key in info:
    print(info[key])

print(info['name'])
print(info['phone']['number'])
print(info['email']['hide'])

input = '''
[
    {
    "id" : "001",
    "x" : "2",
    "name" : "Chuck"
    } ,
    {
    "id" : "009",
    "x" : "7",
    "name" : "Brent"
    }
]'''

info = json.loads(input)
print(input)

print(len(input))
for item in info:
    print(item['x'])
    print(item['id'])
    print(item['name'])
