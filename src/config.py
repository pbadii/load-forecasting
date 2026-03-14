"""
Configuration module for Electricity Load Forecasting Project.
Handles API credentials and environment settings securely.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration class for project settings."""
    
    # API Settings
    EIA_API_KEY = os.getenv("EIA_API_KEY")
    EIA_BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/"
    
    # File Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    NOTEBOOKS_DIR = BASE_DIR / "notebooks"
    
    # Ensure directories exist
    @classmethod
    def initialize_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Validation
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present."""
        errors = []
        
        if not cls.EIA_API_KEY:
            errors.append("EIA_API_KEY not found in environment variables")
        
        if errors:
            raise ValueError("\n".join(errors))
        
        return True
    
    @classmethod
    def get_api_params(cls):
        """Return standardized API request parameters."""
        return {
                "frequency": "annual",
                "data": [
                    "all-other-costs",
                    "customer-incentive",
                    "energy-savings",
                    "potential-peak-savings"
                ],
                "facets": {},
                "start": "2024",
                "end": "2024",
                "sort": [
                    {
                        "column": "period",
                        "direction": "desc"
                    }
                ],
                "offset": 0,
                "length": 5000
            }

# Initialize directories on module import
Config.initialize_directories()