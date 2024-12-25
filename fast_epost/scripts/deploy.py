import subprocess
import os

def deploy_to_heroku():
    commands = [
        'git add .',
        'git commit -m "Deploy to Heroku"',
        'git push heroku main'
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True, check=True)

if __name__ == '__main__':
    deploy_to_heroku()
