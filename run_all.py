import subprocess, time

models = ["densenet121", "vgg16", "densenet169", "resnet50", "vgg19"]
thresholds = [65, 70, 100, 200]
runs = 10

for r in range(0, runs):
    for t in thresholds:
        for m in models:

            start = time.time()

            filename = m + "_" + str(t) + "_" + str(r) + ".csv"
            model_command = "/opt/venv/bin/python /root/DeepRecon/models/" + m + ".py"
            p0 = subprocess.Popen(model_command, shell=True)
            print("Inferencing")
            time.sleep(10)
            print("Now starting extraction")

            
            extract_command = "/root/DeepRecon/attacks/flush_reload . " + str(t) + " " + filename
            p1 = subprocess.Popen(extract_command, shell=True)

            done = False
            while not done:
                if p0.poll() is None:
                    print("Inference running...")
                if p1.poll() is None:
                    print("Extraction running...")
                time.sleep(1)
                if (p0.poll() is not None and p1.poll() is not None):
                    done = True

            print("Done! (" + str(time.time() - start) + ")")
