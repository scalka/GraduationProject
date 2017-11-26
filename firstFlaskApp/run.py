#run a test server

from main import app

if __name__ == '__main__':
    # run main on the server this script is directly executed by the Python interpreter, which we ensured using the if statement with __name__ == '__main__'.
    app.run(port=5000, host='localhost', debug=True)