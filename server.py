import threading
import modelserver_pb2_grpc, modelserver_pb2
import torch

class PredictionCache:
    cache_size = 10
    cache = {}
    evict_order = []
    lock = threading.Lock()
    initial_coefs = torch.tensor(0.0)
    
    def SetCoefs(coefs):
        # will store coefs in the PredictionCache object
        cache.clear()
        new_coef = torch.tensor(coefs, dtype=float32) 
        initial_coefs = torch.transpose(new_coef, 0, 1)


    def Predict(X):
        # will take a 2D tensor and use it to predict y values
        with lock:
            hit = False
            X = round(X, 4)
            y = X @ coefs
            X = tuple(X.flatten().tolist())
            if X in cache:
                # HIT
                hit = True
                df = cache[X]
                index = cache.index(X)
                victim = evict_order.pop(index)
                cache = cache.insert(0, X)
            else:
                if len(cache) > cache_size:
                    victim = evict_order.pop(0)
                    cache.pop(victim)
                cache[X] = df

            return y, hit
        
class ModelServer(modelserver_pb2_grpc.ModelServerServicer):
    cache = PredictionCache()
    def SetCoefs(self, request, context):
        try:
            global cache
            cache.SetCoefs(request.coefs)
            return modelserver_pb2.SetCoefsResponse(error = "")
        except:
            return modelserver_pb2.SetCoefsResponse(error = "ModelServer SetCoefs() failed")
    
    def Predict(self, request, context):
        try:
            global cache
            predictY, predictHit = cache.Predict(request.X)
            return modelserver_pb2.PredictResponse(y = predictY, hit = predictHit, error = "")
        except:
            return modelserver_pb2.PredictResponse(error = "ModelServer Predict() failed")
        

# Server Code
import grpc
from concurrent import futures
server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=(('grpc.so_reuseport', 0),))
modelserver_pb2_grpc.add_ModelServerServicer_to_server(ModelServer(), server)
server.add_insecure_port("[::]:5440", )
server.start()
print("started")
server.wait_for_termination()
