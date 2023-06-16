from pathlib import Path
import re
import shutil
from datetime import datetime as dt
import os

scriptPath = os.path.realpath(os.path.dirname(__file__))
os.chdir(scriptPath)
logFile = 'vhost_pop_logs.log'
files = [path for path in Path('containers').rglob('compose.yml')]

def timestamp():
    return dt.now().strftime('%Y/%m/%d %H:%M: ')

def writeLog(logType: str, exception: Exception, object: str):
    if logType == 'error':
        try:
            with open(logFile, 'r+') as f:
                lines = f.readlines()
                if len(lines) > 1000:
                    lines.pop(0)
                    lines.append(f'[{logType}] {timestamp()} Could not add {object}.\n{timestamp()}     Error: {exception}.\n')
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                else:
                    f.writelines(f'[{logType}] {timestamp()} Could not add {object}.\n{timestamp()}     Error: {exception}.\n')
        except Exception as e:
            return e
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
            return e
    else: 
        raise Exception('Invalid log type.')

def main():
    try:
        for file in files:
            with open(file.as_posix()) as f:
                currentFile = f.read()

            rgx = re.search('(?<=VIRTUAL_HOST=).+', currentFile)
            if rgx:
                if (not Path(f'containers/nginx/vhost.d/{rgx[0]}').is_file()) and (rgx[0] != 'DEFAULT_HOST'):
                    print(rgx[0])
                    try:
                        shutil.copy('containers/nginx/vhost.d/isame-lab.com', f'containers/nginx/vhost.d/{rgx[0]}')
                    except Exception as e:
                        writeLog('error', e, rgx[0])
                    else:
                        writeLog('info', '', object=rgx[0])
    except Exception as e:
        return e

if __name__ == '__main__':
    main()