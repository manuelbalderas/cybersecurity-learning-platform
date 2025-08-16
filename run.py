import eventlet
eventlet.monkey_patch()

from app import create_app, socket

eventlet.monkey_patch()

app = create_app()

from datetime import date
@app.context_processor
def inject_today():
    return {'today': date.today()}

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000, debug=True)