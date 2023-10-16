import threading
import modelserver_pb2_grpc, modelserver_pb2
import torch
import numpy as np
import pandas

class PredictionCache:

    def __init__(self):
        self.cache_size = 10
        self.cache = {}
        self.evict_order = []
        self.lock = threading.Lock()
        self.initial_coefs = torch.tensor(0)


    def SetCoefs(self, coefs):
        # will store coefs in the PredictionCache object
        self.cache.clear()
        new_coef = torch.tensor(coefs, dtype=torch.float32)
        self.initial_coefs = new_coef
        print(new_coef)
        print(self.initial_coefs)


    def Predict(self, X):
        # will take a 2D tensor and use it to predict y values
        # torch_X = torch.tensor(X)
        with self.lock:
            hit = False
            roundedX = torch.round(X, decimals=4)
            X = roundedX.to(torch.float32)
            coefs = torch.tensor(self.initial_coefs)
            coefs = coefs.to(torch.float32)
            tupleX = tuple(X.flatten().tolist())
            key_list = self.cache.keys()
            if tupleX in key_list:
                # HIT
                hit = True
                y = self.cache[tupleX]
                self.evict_order.remove(tupleX)
                self.evict_order.append(tupleX)
            else:
                y = X @ coefs
                self.cache[tupleX] = y
                self.evict_order.append(tupleX)
                if len(self.cache) > self.cache_size:
                    victim = self.evict_order.pop(0) # what has been in the queue the longest?
                    self.cache.pop(victim)
            #print(y.size())
            return self.cache[tupleX], hit


class ModelServer(modelserver_pb2_grpc.ModelServerServicer):
    def __init__(self):
        self.cache = PredictionCache()

    def SetCoefs(self, request, context):
        try:
            self.cache.SetCoefs(request.coefs)
            return modelserver_pb2.SetCoefsResponse(error = "")
        except Exception as e:
            print(e)
            return modelserver_pb2.SetCoefsResponse(error = "ModelServer Predict() failed")
    
    def Predict(self, request, context):
        try:
            torch_X = torch.tensor(request.X)
            predictY, predictHit = self.cache.Predict(torch_X)
            #predictY = predict_results[0]
            #predictHit = predict_results[1]
            return modelserver_pb2.PredictResponse(y = predictY, hit = predictHit, error = "")
        except Exception as e:
            return modelserver_pb2.PredictResponse(error = e)
            #return modelserver_pb2.PredictResponse(error = "ModelServer Predict() failed")
        

# Server Code
import grpc
from concurrent import futures
if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=(('grpc.so_reuseport', 0),))
    modelserver_pb2_grpc.add_ModelServerServicer_to_server(ModelServer(), server)
    server.add_insecure_port("[::]:5440", )
    server.start()
    print("started")
    server.wait_for_termination()
