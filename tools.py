# tools.py
# This file contains the mock lead capture function

def mock_lead_capture(name: str, email: str, platform: str) -> str:
    """
    Mock API function to capture lead information.
    In a real app, this would save to a database or CRM.
    """
    print("\n" + "="*50)
    print("✅ LEAD CAPTURED SUCCESSFULLY!")
    print(f"   Name     : {name}")
    print(f"   Email    : {email}")
    print(f"   Platform : {platform}")
    print("="*50 + "\n")
    
    return f"Lead captured successfully for {name} ({email}) on {platform}."