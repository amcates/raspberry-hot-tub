import threading

ready = False

cv = threading.Condition()

with cv:
    while not ready:
        cv.wait()
    print("I'm ready")

with cv:
    ready = True
