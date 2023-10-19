import os

hostname = "google.com"  # example
response = os.system("ping -c 1 " + hostname)
# and then check the response...
if response == 0:
    print(f"{hostname} is up!")
else:
    print(f"{hostname} is down!")
