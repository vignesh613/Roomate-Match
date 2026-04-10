import pandas as pd
import numpy as np
import random

# Define locations in Siruseri IT Park region
locations = [
    "Siruseri", "Navalur", "Kelambakkam", "Sholinganallur", "Thoraipakkam",
    "Perungudi", "Taramani", "Adyar", "Velachery", "Tambaram"
]

# Lifestyle tags
lifestyle_tags = [
    "Non-smoking", "Smoking allowed", "Vegetarian", "Non-vegetarian", "Mixed diet",
    "Early riser", "Night owl", "Flexible schedule", "Pet friendly", "No pets"
]

# Generate 50 listings
data = []
for i in range(50):
    listing = {
        "id": i + 1,
        "location": random.choice(locations),
        "rent": random.randint(4000, 12000),
        "deposit": random.randint(10000, 30000),
        "num_roommates": random.randint(1, 4),
        "vacancy_count": random.randint(1, 3),
        "lifestyle_tags": ", ".join(random.sample(lifestyle_tags, random.randint(2, 4))),
        "contact_info": f"contact{i+1}@example.com",
        "urgency": random.choice(["Immediate Move-in (48 hrs)", "Flexible"]),
        "trust_score": random.randint(50, 100),
        "description": f"A comfortable {random.randint(1,3)}BHK apartment in {random.choice(locations)} with {random.randint(1,4)} roommates. Perfect for working professionals."
    }
    data.append(listing)

df = pd.DataFrame(data)
df.to_csv("c:/Users/dharma sundhara/Capstone Project/data/mock_listings.csv", index=False)
print("Mock listings generated and saved to mock_listings.csv")