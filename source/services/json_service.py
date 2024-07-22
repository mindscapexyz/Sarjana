import json

def manage_json(filename='keys.json'):
    data = {
        "OPENAPI_KEY": "asfghh",
        "MALLAM_KEY": "asdfgh"
    }
    
    # Write to JSON file
    with open(filename, 'w') as f:
        json.dump(data, f)
    
    # Read and print items from JSON file
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
    
    for key, value in loaded_data.items():
        print(f"{key}: {value}")

# Execute the function
manage_json()