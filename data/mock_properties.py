"""
Mock property data generator for testing
"""
from models.property import Property


def get_sample_properties():
    """Returns a list of realistic property scenarios"""
    
    properties = [
        Property(
            property_id="PROP-001",
            address="1234 Maple Street",
            city="Austin",
            state="TX",
            price=425000,
            bedrooms=3,
            bathrooms=2.0,
            sqft=1850,
            year_built=2015,
            property_type="Single Family",
            estimated_rent=2400,
            hoa_fees=0,
            property_tax_annual=8500,
            insurance_annual=1800
        ),
        Property(
            property_id="PROP-002",
            address="567 Ocean View Blvd",
            city="San Diego",
            state="CA",
            price=785000,
            bedrooms=2,
            bathrooms=2.0,
            sqft=1200,
            year_built=2018,
            property_type="Condo",
            estimated_rent=3200,
            hoa_fees=450,
            property_tax_annual=9420,
            insurance_annual=2100
        ),
        Property(
            property_id="PROP-003",
            address="890 Industrial Ave",
            city="Phoenix",
            state="AZ",
            price=320000,
            bedrooms=4,
            bathrooms=2.5,
            sqft=2100,
            year_built=2008,
            property_type="Single Family",
            estimated_rent=2100,
            hoa_fees=0,
            property_tax_annual=3840,
            insurance_annual=1500
        ),
        Property(
            property_id="PROP-004",
            address="2345 Downtown Plaza",
            city="Nashville",
            state="TN",
            price=550000,
            bedrooms=3,
            bathrooms=3.0,
            sqft=1650,
            year_built=2020,
            property_type="Multi-Family",
            estimated_rent=3800,
            hoa_fees=200,
            property_tax_annual=5500,
            insurance_annual=2200
        ),
        Property(
            property_id="PROP-005",
            address="678 Suburban Lane",
            city="Charlotte",
            state="NC",
            price=380000,
            bedrooms=3,
            bathrooms=2.5,
            sqft=1900,
            year_built=2012,
            property_type="Single Family",
            estimated_rent=2200,
            hoa_fees=100,
            property_tax_annual=4560,
            insurance_annual=1600
        )
    ]
    
    return properties


def get_market_data(city: str):
    """Returns mock market data for a given city"""
    
    market_data = {
        "Austin": {
            "appreciation_rate": 8.5,
            "market_heat": "Hot",
            "competition_level": "High",
            "neighborhood_rating": 8.5,
            "school_rating": 8.0,
            "crime_index": 35,
            "avg_price_per_sqft": 245
        },
        "San Diego": {
            "appreciation_rate": 6.2,
            "market_heat": "Warm",
            "competition_level": "High",
            "neighborhood_rating": 9.0,
            "school_rating": 8.5,
            "crime_index": 28,
            "avg_price_per_sqft": 625
        },
        "Phoenix": {
            "appreciation_rate": 9.1,
            "market_heat": "Hot",
            "competition_level": "Medium",
            "neighborhood_rating": 7.5,
            "school_rating": 7.0,
            "crime_index": 42,
            "avg_price_per_sqft": 165
        },
        "Nashville": {
            "appreciation_rate": 7.8,
            "market_heat": "Hot",
            "competition_level": "High",
            "neighborhood_rating": 8.8,
            "school_rating": 8.2,
            "crime_index": 32,
            "avg_price_per_sqft": 335
        },
        "Charlotte": {
            "appreciation_rate": 6.5,
            "market_heat": "Warm",
            "competition_level": "Medium",
            "neighborhood_rating": 8.0,
            "school_rating": 7.8,
            "crime_index": 38,
            "avg_price_per_sqft": 195
        }
    }
    
    return market_data.get(city, market_data["Austin"])
