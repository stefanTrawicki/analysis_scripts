import sys, os

if len(sys.argv) == 1:
    print("Provide docker container ID")

else:
    docker_container = sys.argv[1]
    commands = [
        "docker exec " + docker_container + " rm -rf /root/DeepRecon/models",
        "docker exec " + docker_container + " mkdir /root/DeepRecon/models",
        "docker cp models/* " + docker_container + ":/root/DeepRecon/",
        "docker cp run_all.py " + docker_container + ":/root/DeepRecon/attacks",
        "docker cp flush_reload.c " + docker_container + ":/root/DeepRecon/attacks",
        "docker exec " + docker_container + " cd /root/DeepRecon/attacks && make",
    ]
    for command in commands:
        os.popen(command)
        print("Ran '" + command + "'")