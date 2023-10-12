import modelserver_pb2_grpc, modelserver_pb2
import grpc
import threading

channel = grpc.insecure_channel("localhost:5440")
stub = modelserver_pb2_grpc.ModelServerStub(channel)

resp = stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs = [1.0,2.0,3.0]))

def loopCSV():
    
t1 = threading.Thread(target=loopCSV)
t2 = threading.Thread(target=loopCSV)
t3 = threading.Thread(target=loopCSV)