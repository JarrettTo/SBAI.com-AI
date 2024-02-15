from flask import Flask, jsonify
from main import main

app = Flask(__name__)

@app.route('/get_main_data', methods=['GET'])
def get_main_data():
    # You can modify this function to return specific data if needed
    main()
    data = {
        'message': 'Data generated from main.py'
        # Add more data fields as needed
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
