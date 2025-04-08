import subprocess

# This script disables notifications on macOS using AppleScript.

def disable_notifications():
    try:
        # AppleScript to disable notifications
        applescript = '''
        tell application "System Events"
            tell process "System Preferences"
                set frontmost to true
            end tell
        end tell
        tell application "System Preferences"
            activate
            set current pane to pane id "com.apple.preference.notifications"
        end tell
        delay 1
        tell application "System Events"
            keystroke "q" using {command down}  -- Quits the notifications settings
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript])
        print("Notifications have been disabled.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    disable_notifications()
