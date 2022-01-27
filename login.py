import cgi
import cgitb
cgitb.enable()

from templates import login_page, secret_page,after_login_incorrect
import secret
import os
from http.cookies import SimpleCookie
import json
s = cgi.FieldStorage()
username = s.getfirst("username")
password = s.getfirst("password")

# print("Content-Type: application/json")
# print()
# print(json.dumps(dict(os.environ),indent=2))
form_ok = username == secret.username and password == secret.password

cookie = SimpleCookie(os.environ["HTTP_COOKIE"])
cookie_username = None
cookie_password = None
if cookie.get("username"):
    cookie_username = cookie.get("username").value
if cookie.get("password"):
    cookie_password = cookie.get("password").value

cookie_ok = cookie_username == secret.username and cookie_password == secret.password

if cookie_ok:
    username = cookie_username
    password = cookie_password


print("Content-Type: text/html")
print()
print(f"<p>HTTP_USER_AGENT={os.environ['HTTP_USER_AGENT']}</p>")

if form_ok:
    print(f"Set-Cookie: username={username}")
    print(f"Set-Cookie: password={password}")


if not username and not password:
    print(login_page())
elif username == secret.username and password == secret.password:
    print(secret_page(username,password))
else:
    print(after_login_incorrect())
