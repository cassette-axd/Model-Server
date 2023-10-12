import threading
import modelserver_pb2_grpc, modelserver_pb2

class PredictionCache:
    cache_size = 10
    cache = {}
    evict_order = []
    lock = threading.Lock()

    def __init__(self):
        self.obj = None
    
    def SetCoefs(coefs):
        # will store coefs in the PredictionCache object
        cache.clear()
        self.obj = coefs


    def Predict(X):
        # will take a 2D tensor and use it to predict y values
        with lock:
            hit = False
            X = round(X, 4)
            y = X @ coefs
            X = tuple(X.flatten().tolist())
            if x in cache:
                # HIT
                hit = True
                df = cache[X]
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
            cache.SetCoefs(request.coefs)
            return modelserver_pb2.SetCoefsResponse(error = "")
        except:
            return modelserver_pb2.SetCoefsResponse(error = "ModelServer SetCoefs() failed")
    
    def Predict(self, request, context):
        try:
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
