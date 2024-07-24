# Ex 13.4: Parsing XML

#
import xml.etree.ElementTree as ET
data = '''<person>
    <name>Chuck</name>
    <phone type="intl">+1 73 303 4456</phone>
    <email hide="yes"/>
</person>'''
print(data)

tree = ET.fromstring(data)
print(tree.find('name').text)
print(tree.find('email').get('hide'))
print()

#
input = '''<stuff>
    <users>
        <user x="2">
            <id>16101020</id>
            <name>Arafe Zawad Sajid</name>
        </user>
        <user x="7">
            <id>16101025</id>
            <name>Anafe Azad Sami</name>
        </user>
    </users>
</stuff>'''

stuff = ET.fromstring(input)
user_list = stuff.findall('users/user')
print(len(user_list))
for user in user_list:
    print(user.get('x'))
    print(user.find('id').text)
    print(user.find('name').text)
