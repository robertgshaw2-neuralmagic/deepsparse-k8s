import requests, argparse, threading

parser = argparse.ArgumentParser()
parser.add_argument("--num_streams", type=int, default=1)
parser.add_argument("--ip", type=str, default="localhost")
parser.add_argument("--iters", type=int, default=100)

class ExecutorThread(threading.Thread):
    def __init__(self, iters, url, obj):
        super(ExecutorThread, self).__init__()
        self.iters = iters
        self.url = url
        self.obj = obj

    def run(self):
        for _ in range(self.iters):
            _ = requests.post(self.url, json=self.obj)

def run(num_streams, ip, iters):
    url = f"http://{ip}:80/predict"
    obj = {"sequences": "Snorlax loves my Tesla!"}
    
    threads = [ExecutorThread(iters, url, obj) for _ in range(num_streams)] 

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
if __name__ == "__main__":
    args = parser.parse_args()
    run(num_streams=args.num_streams, ip=args.ip, iters=args.iters)

