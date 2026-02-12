


from google.cloud import firestore
from datetime import datetime
import pytz

# Set Israel timezone
israel_tz = pytz.timezone("Asia/Jerusalem")

print("🚀 Connecting to Firestore database 'firestore-accounts-db'...")

# Initialize Firestore client using gcloud auth (no JSON key)
db = firestore.Client(
    # 🔹 Replace with your real GCP project ID
    # project="dgt-gcp-cgov-d-datapro", 
    # project="dgt-gcp-cgov-d-i-binom",       
    project="labor-459609",
    # 🔹 Firestore DB name created by Terraform
    database="firestore-accounts-db-temporary"      
    
)

# Define 3 example government-related accounts
accounts_data = [
    {
        "MinistryName": "shikun",             # משרד השיכון
        "ProjectName": "syua-bediyur",
        "bucket_sub_path": "shikun",
        "x-client-id": "100",
        "x-client-secret": "secret",
        "x-scope": "1234"
    },
    {
        "MinistryName": "labor",              # משרד העבודה
        "ProjectName": "employment-center",
        "bucket_sub_path": "labor",
        "x-client-id": "200",
        "x-client-secret": "secret",
        "x-scope": "5678"
    },
    {
        "MinistryName": "treasury",           # משרד האוצר
        "ProjectName": "tax-division",
        "bucket_sub_path": "treasury",
        "x-client-id": "300",
        "x-client-secret": "secret",
        "x-scope": "9012"
    },
        {
        "MinistryName": "Agency",           #כללי
        "ProjectName": "SubDivision",
        "bucket_sub_path": "test",
        "x-client-id": "123",
        "x-client-secret": "secret",
        "x-scope": "321"
    }

]

# Insert each document
for entry in accounts_data:
    # Timestamp in Israel timezone
    now = datetime.now(israel_tz)
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")

    # Simulated ClientRequestId pattern
    # client_request_id = f"{entry['x-client-id']}-{entry['x-scope']}_{timestamp_str}"

    # Construct DnaTransactionId
    # dna_transaction_id = f"{entry['AgencyId']}_{entry['SubdivisionId']}_{client_request_id}"

    entry["CreatedAt"] = now.isoformat()
    # entry["ClientRequestId"] = client_request_id
    # entry["DnaTransactionId"] = dna_transaction_id

    # Deterministic document ID for re-updates
    doc_id = f"{entry['x-client-id']}_{entry['x-scope']}"
    doc_ref = db.collection("accounts").document(doc_id)

    if not doc_ref.get().exists:
        doc_ref.set(entry)
        print(f"✅ Created document: {doc_id}")
    else:
        print(f"ℹ️ Document already exists: {doc_id}, updating data...")
        doc_ref.update(entry)

print("🎉 Firestore 'accounts' collection initialized successfully with 3 Israeli agency examples.")