from pathlib import Path
import re
import shutil
from datetime import datetime as dt
import os

# NOTE: This script must be run adjacent to top directory where you want to locate compose files.

# Change these. Do not append paths with a /.
defaultHost = 'isame-lab.com'
defaultVhost = 'proxy_set_header Upgrade $http_upgrade;\nproxy_set_header Connection "upgrade";\nproxy_http_version 1.1;'
logFile = 'vhost_pop_logs.log'
containersPath = 'containers'
vhostPath = 'containers/nginx/vhost.d'

# Determining script's path and changes to it. Makes paths a bit easier. 
scriptPath = os.path.realpath(os.path.dirname(__file__))
os.chdir(scriptPath)

# Creating the log file if it doesn't exist.
try:
    if not os.path.exists(logFile):
        with open(logFile, 'w'): pass
except Exception as e:
    raise e

# Throw errors if vital paths do not exist.
if not os.path.exists(containersPath):
    raise Exception(f'Directory {containersPath} not present.')
if not os.path.exists(vhostPath):
    raise Exception(f'Directory {vhostPath} not present.')

# Finding all compose files.
files = [path for path in Path(containersPath).rglob('*') if path.name in ('compose.yml', 'docker-compose.yml')]

if not files:
    raise Exception('No compose.yml or docker-compose.yml files found.')

def timestamp():
    # Returns the current time and date as a formatted string.
    return dt.now().strftime('%Y/%m/%d %H:%M: ')

def writeLog(logType: str, exception: Exception, object: str):
    # Takes a log type, and writes to the file depending on the type.
    # Also ensures the log file never exceeds 1000 lines.
    if logType == 'error':
        try:
            with open(logFile, 'r+') as f:
                lines = f.readlines()
                if len(lines) > 1000:
                    lines.pop(0)
                    lines.append(f'[{logType}] {timestamp()} Could not add {object}.\n        Error: {exception}.\n')
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                else:
                    f.writelines(f'[{logType}] {timestamp()} Could not add {object}.\n        Error: {exception}.\n')
        except Exception as e:
            raise e
    elif logType == 'info':
        try:
            with open(logFile, 'r+') as f:
                lines = f.readlines()
                if len(lines) > 1000:
                    lines.pop(0)
                    lines.append(f'[{logType}] {timestamp()} Added {object}.\n')
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                else:
                    f.writelines(f'[{logType}] {timestamp()} Added {object}.\n')
        except Exception as e:
            raise e
    else: 
        raise Exception('Invalid log type.')

def main():
    # Writing default inital host file if it doesn't exist. 
    try:
        if not os.path.exists(f'{vhostPath}/{defaultHost}'):
            try:
                with open(f'{vhostPath}/{defaultHost}', 'w') as f:
                    f.write(defaultVhost)
            except:
                return Exception(f'Unable to write initial vhost file.\n{e}')
    except Exception as e:
        return Exception(f'Unable to locate or create initial vhost file.\n{e}')
    # Checks for VIRTUAL_HOST environment variable in all found compose files. If one is present, checks if the corresponding vhost file exists. If not, creates it using the default.
    try:
        for file in files:
            with open(file.as_posix()) as f:
                currentFile = f.read()

            rgx = re.search('(?<=VIRTUAL_HOST=).+', currentFile)
            if rgx:
                if (not Path(f'{vhostPath}/{rgx[0]}').is_file()) and (rgx[0] != 'DEFAULT_HOST'):
                    try:
                        shutil.copy(f'{vhostPath}/{defaultHost}', f'{vhostPath}/{rgx[0]}')
                    except Exception as e:
                        writeLog('error', e, rgx[0])
                    else:
                        writeLog('info', '', object=rgx[0])
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()