# il2_chat_monitoring
The goal of this script is to monitor the in game chat in order to answer by automated actions.
The current application is to launch artillery strikes using this system: https://github.com/Super-truite/il2_artillery_RC
If you need to perform other actions anf know the python language, you can modify the detect_commands function in monitor_chat.py 

## Remote console: Before installing, please make sure you know how to use and setup the il2 remote console.
Please follow the instructions p:173 of JimTM's guide (https://forum.il2sturmovik.com/topic/26303-il-2-sturmovik-mission-editor-and-multiplayer-server-manual/)
to setup your remote console. 

## Download the release executable
Download and extract the .zip of the latest release here: https://github.com/Super-truite/il2_chat_monitoring/releases

## Configure
In the dist sub folder, in the config.ini file, fill the information regarding your remote console, who you want to be able to use the artillery
and the IL2 data path of your server?
The file shoul look like this:
```
[DEFAULT]
REMOTE_CONSOLE_IP = my_ip
REMOTE_CONSOLE_PORT = 8991
ALLOWED_CALLERS = super-truite,clem64121,ickylevel
LOGIN_REMOTE_CONSOLE = my_login
PASSWORD_REMOTE_CONSOLE = my_password
IL2_DATA_PATH = D:\\IL2Dserver\\IL-2 Sturmovik Great Battles\\data\\
```
Names of the allowed callers are the ingame names