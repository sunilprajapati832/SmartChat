import eventlet
eventlet.monkey_patch()   # MUST be first line

from app import app, socketio

if __name__ == "__main__":
    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True
    )