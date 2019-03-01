from communication import WebConnectionManager

w = WebConnectionManager.WebConnectionManager()
w.daemon = True
w.start()
input()
