# Ex 13.5 - JavaScript Object Notation (JSON)
import json

# parsing to a dictionary of dictionaries
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

# load from string method
info = json.loads(data)  # info is a dictionary of dictionaries
print(info['name'])
print(info["email"]["hide"], '\n')  # dictionary within a dictionary

# parsing to a list of dictionaries
data = '''
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

info = json.loads(data)  # info is a list of dictionaries
print(len(info))  # length of string
for item in info:
    print(item['name'])
    print(item['id'])
    print(item['x'])
print()
# ---------------------------------------
