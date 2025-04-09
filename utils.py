import uuid
import datetime
import random
from datetime import datetime, timedelta

# Initialize list of 25 sample users with conversation histories
def initialize_users():
    users = {}
    
    for i in range(25):
        # Generate unique user_id
        user_id = str(uuid.uuid4())
        username = f"user_{user_id}"
        
        # Generate sample conversation history
        sample_conversation = [
            {
                "role": "user",
                "content": "What are the best places to visit in Silicon Valley?",
                "timestamp": (datetime.now() - timedelta(days=random.randint(1,30))).isoformat()
            },
            {
                "role": "assistant", 
                "content": "Some key places to visit include Stanford University, Computer History Museum, Google campus, and Apple Park Visitor Center.",
                "timestamp": (datetime.now() - timedelta(days=random.randint(1,30))).isoformat()
            }
        ]
        
        # Create user entry
        users[username] = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "conversation_history": sample_conversation,
            "number_of_messages": len(sample_conversation),
            "logged": False
        }
    
    return users
