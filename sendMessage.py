import subprocess

def text(phoneNumber, message):
    """Takes in two strings: phone number and message, and sends through SMS"""
    subprocess.run(['osascript', '-e', '''
    on run argv
        tell application "Messages"
            set targetBuddy to (item 1 of argv)
            set targetService to id of 1st account whose service type = SMS
            set textMessage to (item 2 of argv)
            set theBuddy to participant targetBuddy of account id targetService
            send textMessage to theBuddy
        end tell
    end run
    ''', phoneNumber, message])


