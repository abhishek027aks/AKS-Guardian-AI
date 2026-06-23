import os
import shutil

def clean_temp():
    temp = os.environ.get("TEMP")

    count = 0

    for item in os.listdir(temp):
        path = os.path.join(temp, item)

        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

            count += 1
        except:
            pass

    return count

def flush_dns():
    os.system("ipconfig /flushdns")