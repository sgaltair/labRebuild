from vhostPop import *


def writeLog(logType: str, logText: str):
    try:
        with open(LOG_FILE_PATH, "r+") as f:
            lines = f.readlines()
            if len(lines) > 1000:
                lines.pop(0)
                lines.append(f"[{logType}] {timestamp()} {logText}\n")
                f.seek(0)
                f.truncate()
                f.writelines(lines)
            else:
                f.writelines(f"[{logType}] {timestamp()} {logText}\n")
    except Exception as e:
        raise e
