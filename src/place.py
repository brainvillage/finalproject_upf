import random

class Place:
    
    def __init__(self, place_id, host_id, city):
        
        # Initialize Args
        self.place_id = place_id
        self.host_id = host_id
        self.city = city
        
        # Initialize attributes that will be set by setup()
        self.neighbours = []
        self.area = None
        self.rate = None
        self.price = {}
        self.occupancy = None
        
        # Call setup to initialize key attributes
        self.setup()
    
    def setup(self):
        
        # Set neighbours (list of adjacent place_ids)
        # This would typically be calculated based on grid position
        # For now, initializing as empty list - would need city grid logic
        self.neighbours = []
        
        # Set area (quadrant): 0=bottom-left, 1=bottom-right, 2=top-left, 3=top-right
        # This would be determined by the place's position in the city grid
        # For now, randomly assigning - would need actual grid position logic
        self.area = random.randint(0, 3)
        
        # Set rate: nightly price from the area's rate interval
        if hasattr(self.city, 'area_rates') and self.area in self.city.area_rates:
            rate_min, rate_max = self.city.area_rates[self.area]
            self.rate = random.uniform(rate_min, rate_max)
        else:
            # Default rate if city doesn't have area_rates defined
            self.rate = random.uniform(50, 200)
        
        # Initialize price dictionary with step 0
        self.price = {0: 900 * self.rate}
        
        # Initialize occupancy
        self.occupancy = None
    
    def update_occupancy(self):
        
        # Calculate mean rate for the area
        if hasattr(self.city, 'get_area_mean_rate'):
            area_mean_rate = self.city.get_area_mean_rate(self.area)
        else:
            # Fallback: calculate from area_rates if available
            if hasattr(self.city, 'area_rates') and self.area in self.city.area_rates:
                rate_min, rate_max = self.city.area_rates[self.area]
                area_mean_rate = (rate_min + rate_max) / 2
            else:
                # Default mean rate
                area_mean_rate = 125
        
        # Set occupancy based on rate comparison
        if self.rate > area_mean_rate:
            # Above average rate: lower occupancy (5-15 days)
            self.occupancy = random.randint(5, 15)
        else:
            # Below or equal to average rate: higher occupancy (10-20 days)
            self.occupancy = random.randint(10, 20)
    
    def __str__(self):
        return f"Place(id={self.place_id}, host={self.host_id}, area={self.area}, rate={self.rate:.2f})"
    
    def __repr__(self):
        return f"Place(place_id={self.place_id}, host_id={self.host_id}, area={self.area}, rate={self.rate:.2f}, occupancy={self.occupancy})"