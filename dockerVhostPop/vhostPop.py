from pathlib import Path
import re
import shutil
from datetime import datetime as dt
import os

from vhostPopConfig import *
from linodeRecordCreate import *

# Checks target directory recursively for compose files with a VIRTUAL_HOST environment variable and creates the corresponding vhost file in the target vhost directory.
# Written to be run alongside nginxproxy/nginx-proxy from https://hub.docker.com/r/nginxproxy/nginx-proxy.
# I run it as a cron job to automate new host creation while 

# If LINODE_INTEGRATION is set to True, also attempts to create the domain record.

# Determining script's path and changes to it. Makes paths a bit easier. 
scriptPath = os.path.realpath(os.path.dirname(__file__))
os.chdir(scriptPath)

# Creating the log file if it doesn't exist.
try:
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w'): pass
except Exception as e:
    raise e

# Throw errors if vital paths do not exist.
if not os.path.exists(f'../{CONTAINERS_PATH}'):
    raise Exception(f'Directory {CONTAINERS_PATH} not present.')
if not os.path.exists(f'../{VHOSTD_PATH}'):
    raise Exception(f'Directory {VHOSTD_PATH} not present.')

# Finding all compose files.
files = [path for path in Path(f'../{CONTAINERS_PATH}').rglob('*') if path.name in ('compose.yml', 'docker-compose.yml')]
if not files:
    raise Exception('No compose.yml or docker-compose.yml files found.')

def timestamp():
    # Returns the current time and date as a formatted string.
    return dt.now().strftime(TIMESTAMP_FORMAT)

def writeLog(logType: str, exception: Exception, object: str):
    # Takes a log type, and writes to the file depending on the type.
    # Also ensures the log file never exceeds 1000 lines.
    if logType == 'error':
        try:
            with open(LOG_FILE_PATH, 'r+') as f:
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
            with open(LOG_FILE_PATH, 'r+') as f:
                lines = f.readlines()
                if len(lines) > 1000:
                    lines.pop(0)
                    lines.append(f'[{logType}]  {timestamp()} Added vhost {object}.\n')
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                else:
                    f.writelines(f'[{logType}]  {timestamp()} Added vhost {object}.\n')
        except Exception as e:
            raise e
    else: 
        raise Exception('Invalid log type.')

def main():
    # Writing default initial host file if it doesn't exist. 
    try:
        if not os.path.exists(f'../{VHOSTD_PATH}/{DEFAULT_HOST}'):
            try:
                with open(f'../{VHOSTD_PATH}/{DEFAULT_HOST}', 'w') as f:
                    f.write(DEFAULT_VHOST_TEXT)
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
                if (not Path(f'../{VHOSTD_PATH}/{rgx[0]}').is_file()) and (rgx[0] != 'DEFAULT_HOST'):
                    try:
                        shutil.copy(f'../{VHOSTD_PATH}/{DEFAULT_HOST}', f'../{VHOSTD_PATH}/{rgx[0]}')
                    except Exception as e:
                        writeLog('error', e, rgx[0])
                    else:
                        writeLog('info', '', object=rgx[0])
                    if LINODE_INTEGRATION:
                        if not createRecord(rgx[0].split('.')[0], 'A'):
                            try:
                                with open(LOG_FILE_PATH, 'r+') as f:
                                    lines = f.readlines()
                                    if len(lines) > 1000:
                                        lines.pop(0)
                                        lines.append(f'[error] {timestamp()} Vhost {rgx[0]} created, but Linode record creation failed.\n')
                                        f.seek(0)
                                        f.truncate()
                                        f.writelines(lines)
                                    else:
                                        f.writelines(f'[error] {timestamp()} Vhost {rgx[0]} created, but Linode record creation failed.\n')
                            except Exception as e:
                                raise e
                        else:
                            try:
                                with open(LOG_FILE_PATH, 'r+') as f:
                                    lines = f.readlines()
                                    if len(lines) > 1000:
                                        lines.pop(0)
                                        lines.append(f'[info]  {timestamp()} Successfully created {rgx[0]} domain record.\n')
                                        f.seek(0)
                                        f.truncate()
                                        f.writelines(lines)
                                    else:
                                        f.writelines(f'[info]  {timestamp()} Successfully created {rgx[0]} domain record.\n')
                            except Exception as e:
                                raise e
                else:
                    try:
                        with open(LOG_FILE_PATH, 'r+') as f:
                            lines = f.readlines()
                            if len(lines) > 1000:
                                lines.pop(0)
                                lines.append(f'[info]  {timestamp()} Run complete - No new hosts found.\n')
                                f.seek(0)
                                f.truncate()
                                f.writelines(lines)
                            else:
                                f.writelines(f'[info]  {timestamp()} Run complete - No new hosts found.\n')
                    except Exception as e:
                        raise e
                            
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()