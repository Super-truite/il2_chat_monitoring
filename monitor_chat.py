import os, re, time, shutil
from remote_console import RemoteConsoleClient
from remote_console_actions import call_command, safe_call_command
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
path =  config['DEFAULT']['IL2_DATA_PATH']
password =  config['DEFAULT']['PASSWORD_REMOTE_CONSOLE']
ALLOWED_CALLERS = [str(x) for x in config['DEFAULT']['ALLOWED_CALLERS'].split(',')]
path_save = os.path.join(path,'save_chatlog')
if not os.path.exists(path_save):
        os.makedirs(path_save)

VERBOSE = False

def list_chatlog():
    l = []
    for file in os.listdir(path):
        if file.endswith(".chatlog"):
            l.append(os.path.join(path, file))
    return l

def clean_chat_log():
    for f in os.listdir(path):
        if f.endswith(".chatlog"):
            try:
                os.remove(os.path.join(path, f))
            except OSError as e:
                #print(e)
                pass
            except:
                raise

def parse_chatfile(chatfile):
    with open(chatfile, 'r') as file:
        lines = file.readlines()
        parsed = []
        for line in lines:
            try:
                result = re.search(r"\[(.*?)\]", line).group(1)
                if len(result) > 0:
                    result = result.split()
                    author, coalition, receiver = result[0], result[2], result[4]
                    timeMessage = line.split(' [')[0]
                    message = line.split(':')[-1]
                    mission = chatfile.split('\\')[-1].split('.')[0]
                    parsed.append({"author": author, "coalition": coalition, "receiver": receiver, "timeMessage": timeMessage, "message": message, "mission": mission})
                    if VERBOSE:
                        print(author, coalition, receiver)
                        print(timeMessage)
                        print(message)
                        print(mission)
                        print("###################")
            except:
                print('Format not taken into account: ', line)
    return parsed
        

def save_chat(List_parsed):
    List_parsed2 = List_parsed.copy()
    l = list_chatlog()
    for chatfile in l:
        if chatfile in List_parsed:
            try:
                shutil.move(chatfile, os.path.join(path_save, chatfile.split("\\")[-1]))
                List_parsed2.remove(chatfile)
            except:
                pass
    return List_parsed2

def save_chat(List_parsed):
    List_parsed2 = List_parsed.copy()
    l = list_chatlog()
    for chatfile in l:
        try:
            shutil.move(chatfile, os.path.join(path_save, chatfile.split("\\")[-1]))
            List_parsed2.remove(chatfile)
        except:
            pass
    return List_parsed2

def detect_commands(parsed_messages):
    print(parsed_messages)
    for a in parsed_messages:
        if 'request artillery at grid' in a["message"]:
            if a["receiver"] == "COALITION":
                # TODO: allowed artillery players
                if a["author"].replace('"', '') in ALLOWED_CALLERS:
                    grid, key, subkey, subsubkey = tuple(a["message"].split('request artillery at grid ')[-1].split())
                    # Allies
                    if a["coalition"] == "1":
                        command = '$RC serverinput artillery_allies_{0}_{1}_{2}_{3}'.format(grid, key, subkey, subsubkey)
                        safe_call_command(command)
                        time.sleep(2)
                        safe_call_command('$RC chatmsg 3 1 Thunder: Copy, Firing at grid {0} {1} {2} {3}'.format(grid, key, subkey, subsubkey))
                    # Axis
                    if a["coalition"] == "2":
                        command = '$RC serverinput artillery_axis_{0}_{1}_{2}_{3}'.format(grid, key, subkey, subsubkey)
                        safe_call_command(command)
                        time.sleep(2)
                        safe_call_command('$RC chatmsg 3 2 Thunder: Copy, Firing at grid {0} {1} {2} {3}'.format(grid, key, subkey, subsubkey))
                else:
                    safe_call_command('$RC chatmsg {0} COALITION Server: You are not authorized to use the artillery, please ask an admin!'.format(a["coalition"]))    
            else:
                safe_call_command('$RC chatmsg {0} COALITION Server: You need to use those commands in coalition chat, not general chat!'.format(a["coalition"]))


call_command('$RC cutchatlog')
time.sleep(2)
save_chat([])      
while(True):
    mission = ''
    call_command('$RC cutchatlog')
    l = list_chatlog()
    for chatfile in l:
        with open(chatfile, 'r') as file:
         parsed_messages = parse_chatfile(chatfile)
         # Code to react to the messages goes here
         detect_commands(parsed_messages)
    save_chat([]) 
    time.sleep(2)


