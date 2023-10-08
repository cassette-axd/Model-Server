import threading

class PredictionCache:
    cach_size = 10
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
                if len(cache) > cach_size:
                    victim = evict_order.pop(0)
                    cache.pop(victim)
                cache[X] = df

            return y, hit


