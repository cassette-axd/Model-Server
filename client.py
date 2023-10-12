import modelserver_pb2_grpc, modelserver_pb2
import grpc
import threading
import sys
import pandas as pd


channel = grpc.insecure_channel("localhost:" + sys.argv[0])
stub = modelserver_pb2_grpc.ModelServerStub(channel)

coefsList =  list(map(int, sys.argv[1].split(",")))
resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = coefsList))
mainThread = threading.Thread()
mainThread.start()
def loopCSV(file):
    df = pd.read_csv(file)
    total = 0
    totalHits = 0
    for index, row in df.iterrows:
        y, hit = stub.Prediction(row)
        if (hit):
            totalHits += 1
        total += 1
    print(totalHits/total)
    totalMisses = totalHits-total

threads = []
for n in range(2, sys.argv.count-1):
    t = threading.Thread(target=loopCSV, args=sys.argv[n])
    t.start()
    threads.append(t)

for i in threads:
    threads[i].join()

mainThread.join()