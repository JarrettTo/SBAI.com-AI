from flask import Flask, request, jsonify
from main import main  # Import the main function from your prediction script

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the request (if needed)
    data = request.json

    # Call the main function from your prediction script
    main()

    # Return a response (if needed)
    return jsonify({"message": "Prediction complete"})

if __name__ == '__main__':
    app.run(debug=True)
