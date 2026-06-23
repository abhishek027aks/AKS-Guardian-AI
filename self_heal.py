import os
import shutil
import tempfile
import subprocess

def clean_temp():
    deleted = 0

    temp_dir = tempfile.gettempdir()

    for item in os.listdir(temp_dir):
        path = os.path.join(temp_dir, item)

        try:
            if os.path.isfile(path):
                os.remove(path)
                deleted += 1

            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                deleted += 1

        except:
            pass

    return deleted


def flush_dns():
    try:
        subprocess.run(
            "ipconfig /flushdns",
            shell=True,
            capture_output=True
        )

        return True

    except:
        return False