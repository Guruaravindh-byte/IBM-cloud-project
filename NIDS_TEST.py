import requests
import json

# 🔑 Replace with your actual API key
API_KEY = "sdGBta9E2GcHT0WcprZ4AjKZuW81sWW9kDLCGUrlHyN7"

# 🌐 Replace with your deployment scoring URL (private/public endpoint)
DEPLOYMENT_URL = "https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/7292523c-00c2-4a49-89fa-158e2917c9b9/predictions?version=2021-05-01"

# 🔐 Get the access token
token_response = requests.post(
    'https://iam.cloud.ibm.com/identity/token',
    data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
)

if token_response.status_code != 200:
    print("❌ Failed to get token")
    print("Status Code:", token_response.status_code)
    print("Response:", token_response.text)
    exit()

mltoken = token_response.json().get("access_token")
if not mltoken:
    print("❌ access_token not found! Check if the API key is wrong or expired.")
    exit()

print("✅ Token received successfully.")

# 🧾 Define the 41 features in order
fields = [
     "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
        "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
        "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
        "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login",
        "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
        "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
        "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
        "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

# 🧪 Sample values from your dataset (must be strings or correct data types)
values = [
    [0, "tcp", "http", "SF", 181, 5450, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 9, 9, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 9, 9, 1.0, 0.0,0.11, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0, "udp", "private", "REJ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 0.0, 0.0, 1.0, 1.0,0.17, 0.0, 0.0, 1, 2, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
          [0, 'tcp', 'private', 'S0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 123, 6, 1.0, 1.0, 0.0, 0.0, 0.05, 0.07, 0.0, 255, 26, 0.1, 0.05, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0]
]

# 📦 Prepare payload
payload_scoring = {
    "input_data": [
        {
            "fields": fields,
            "values": values
        }
    ]
}

# 📡 Send the scoring request
response_scoring = requests.post(
    DEPLOYMENT_URL,
    json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken}
)

print("✅ Scoring Response:")
try:
    print(json.dumps(response_scoring.json(), indent=2))
except Exception as e:
    print("⚠️ Error reading response:", e)
