import os

print("Push to GitHub")
os.system('git push')
print("Change directory to submodule")
os.system("cd ~/skillhub/skillhub/")
print("Push to Heroku")
os.system("git push heroku master:master")
