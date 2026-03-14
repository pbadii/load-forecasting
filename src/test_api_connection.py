"""
Test script to verify EIA API connection and credentials.
Run this before starting data ingestion to ensure everything is configured correctly.
"""

import requests
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config

def test_api_connection():
    """
    Test the EIA API connection with a minimal request.
    Returns True if successful, False otherwise.
    """
    print("=" * 60)
    print("Testing EIA API Connection")
    print("=" * 60)
    
    # Validate configuration first
    try:
        Config.validate_config()
        print("✓ Configuration validated successfully")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        return False
    
    # Make a test request with minimal data
    params = Config.get_api_params()
    params['facets'] = {'region_type': ['T']}
    params['limit'] = 5  # Only fetch 5 records for testing
    
    print(f"\n📡 Sending request to: {Config.EIA_BASE_URL}")
    print(f"📊 Request parameters: frequency={params['frequency']}, limit={params['limit']}")
    
    try:
        response = requests.get(Config.EIA_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we got valid data
        if 'response' in data and 'data' in data['response']:
            records = data['response']['data']
            print(f"\n✓ API connection successful!")
            print(f"✓ Received {len(records)} test record(s)")
            
            # Display sample record structure
            if records:
                print(f"\n📋 Sample record structure:")
                for key in records[0].keys():
                    print(f"   - {key}")
            
            return True
        else:
            print("\n✗ Unexpected API response structure")
            print(f"Response keys: {list(data.keys())}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n✗ Request timed out (30 seconds)")
        print("   Check your internet connection")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"\n✗ HTTP Error: {e.response.status_code}")
        print(f"   Details: {e.response.text[:200]}")
        
        if e.response.status_code == 403:
            print("   ⚠️  Possible causes:")
            print("      - Invalid or expired API key")
            print("      - API key not properly formatted")
            print("      - Rate limit exceeded")
        elif e.response.status_code == 401:
            print("   ⚠️  Authentication failed - check your API key")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

def main():
    """Main execution function."""
    success = test_api_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! Ready to proceed with data ingestion.")
        print("\nNext steps:")
        print("   1. Create src/data_loader.py for full data download")
        print("   2. Begin Week 1: Data Ingestion & Exploration")
    else:
        print("❌ Tests failed. Please review the errors above.")
        print("\nTroubleshooting tips:")
        print("   1. Verify .env file exists in project root")
        print("   2. Check EIA_API_KEY format (no extra spaces)")
        print("   3. Confirm API key is active at https://www.eia.gov/tools/api/")
        print("   4. Ensure python-dotenv is installed (pip install python-dotenv)")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())