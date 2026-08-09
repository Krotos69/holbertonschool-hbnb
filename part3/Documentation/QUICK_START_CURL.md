🚀 Quick Start Guide for cURL Testing
Step 1: Start the Flask Server
Open a terminal in WSL/Linux and run:

# Navigate to the project
cd /mnt/d/myschoolworkandGithub/holbertonschool-hbnb/part2/hbnb

# Activate virtual environment
source ../../hbnb-venv/bin/activate

# Start the Flask server
python run.py
You should see output like:

 * Running on http://127.0.0.1:5000
 * Debug mode: on
Step 2: Test with cURL (in a new terminal)
Open a new terminal (keep the Flask server running in the first one) and run:

Quick Test Commands:
# Test 1: Check if API is running
curl http://localhost:5000/api/v1/

# Test 2: Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john@example.com"
  }'

# Test 3: Get all users
curl http://localhost:5000/users

# Test 4: Create an amenity
curl -X POST http://localhost:5000/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'

# Test 5: Get all amenities
curl http://localhost:5000/amenities
Step 3: Run the Automated Test Script
# Make sure you're in the hbnb directory
cd /mnt/d/myschoolworkandGithub/holbertonschool-hbnb/part2/hbnb

# Run the test script
./test_api.sh
Step 4: Explore the Swagger UI
Open your browser and go to: http://localhost:5000/api/v1/

This will show you the interactive API documentation where you can test endpoints directly in the browser.

🔧 Troubleshooting
Port already in use: Kill the process with pkill -f "python run.py" and restart
Connection refused: Make sure Flask server is running in the first terminal
Import errors: Ensure virtual environment is activated
📖 More Testing
For comprehensive testing examples, see: CURL_TESTING_GUIDE.md