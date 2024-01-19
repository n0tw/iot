import subprocess, time

def run_busai(script_path, arguments):
    command = ['python', script_path] + arguments

    try:
        subprocess.Popen(command)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
busai_script = "C:/Users/pangl/Desktop/GitRepo/bus-raspberry/busai.py"
ids = []
i=1

while i <6:
    ids.append(['urn:ngsi-ld:Vehicle:vehicle:Bus:'+str(i), 'urn:ngsi-ld:CrowdFlowObserved:Bus:'+str(i)])
    run_busai(busai_script, ids[-1])
    i+=1
    time.sleep(240)



