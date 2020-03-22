
json = {
  "user": {
    "name": "brunoibez"
  },
  "text": "140 carácteres del usuario..",
  "entities": {
    "urls": [
      {
        "url": "www.google.com"
      }
    ]
  }
}


output = ""
output += "Tweet por @%s\n" % (json["user"]["name"])
output += "%s\n" % (json["text"])
output += "%s" % (json["entities"]["urls"][0]["url"])

print(output)
