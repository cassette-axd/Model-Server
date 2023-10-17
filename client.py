import modelserver_pb2_grpc
import modelserver_pb2
import grpc
import threading
import sys
import pandas as pd
import torch
import numpy as np

channel = grpc.insecure_channel(f"localhost:{sys.argv[1]}")
stub = modelserver_pb2_grpc.ModelServerStub(channel)
coefsList = list(map(float, sys.argv[2].split(",")))

resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = coefsList))
mainThread = threading.Thread()
mainThread.start()
all_hits = 0
all_misses = 0
total = 0
lock = threading.Lock()

# Loops through CSV and uses a cache to calculate the hit rate
def loopCSV(file):
    with lock:
        df = pd.read_csv(file, header=None)
        global all_hits
        global all_misses
        global total
        for index, row in df.iterrows():
            float_values = [float(value) for value in row]
            response_predict = stub.Predict(modelserver_pb2.PredictRequest(X = float_values))
            if (response_predict.hit):
                all_hits += 1
            else:
                all_misses +=1

# Creates a variable amount of threads based on the number of arguments
threads = []
try:
    for n in range(3, len(sys.argv)):
        t = threading.Thread(target=loopCSV, args=(sys.argv[n],))
        t.start()
        threads.append(t)
finally:
    for i in threads:
        i.join()

mainThread.join()
if (all_misses + all_hits) == 0:
    print(0)
else:
    print(all_hits/(all_hits + all_misses))
