import modelserver_pb2_grpc
import modelserver_pb2
import grpc
import threading
import sys
import pandas as pd

#channel = grpc.insecure_channel("localhost:5440" + sys.argv[1])
channel = grpc.insecure_channel("localhost:" + sys.argv[1])
stub = modelserver_pb2_grpc.ModelServerStub(channel)
coefsList =  list(map(float, sys.argv[2].split(",")))
#resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = [1.0,2.0,3.0]))
#resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = [1.0,2.0,3.0]))

#channel = grpc.insecure_channel("localhost:" + sys.argv[0])
#stub = modelserver_pb2_grpc.ModelServerStub(channel)

#resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = coefsList))
mainThread = threading.Thread()
mainThread.start()
all_hits = 0
all_misses = 0
def loopCSV(file):
    df = pd.read_csv(file)
    total = 0
    totalHits = 0
    for index, row in df.iterrows():
        print(row)
        y, hit = stub.Predict(row.astype('float32'))
        print(y)
        print(hit)
        if (hit):
            all_hits += 1
        else:
            all_misses +=1
        total += 1

threads = []
try:
#    if len(sys.argv) == 5:
#        t1 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t1.start()
#        threads.append(t1)

#        t2 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t2.start()
#        threads.append(t2)

#        t3 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t3.start()
#        threads.append(t3)
#    else if len(sys.argv) == 4:
#        t1 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t1.start()
#        threads.append(t1)

#        t2 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t2.start()
#        threads.append(t2)
#    else:
#        t1 = threading.Thread(target=loopCSV, args=[sys.argv[n]])
#        t1.start()
#        threads.append(t1)
    for n in range(3, len(sys.argv)):
        print("created")
        t = threading.Thread(target=loopCSV, args=(sys.argv[n],))
        t.start()
        threads.append(t)
finally:
    for i in threads:
        i.join()

mainThread.join()
print(all_hits)
print(all_misses)
print(all_hits/(all_hits + all_misses))
