class Host:
    
    def __init__(self, host_id, place, city, profits=0):
        
        # Inititalize Args
        self.host_id = host_id
        self.city = city
        self.profits = profits
        
        # Host's area is defined as the area of its initial place
        self.area = place.area
        
        # Host's initial place becomes its first asset
        # assets is a set containing the IDs of all properties the host owns
        self.assets = {place.place_id}
    
    def update_profits(self):
        
        for place_id in self.assets:
            # Retrieve the Place object from the city
            place = self.city.get_place(place_id)
            if place is not None:
                # Add monthly earnings: rate * occupancy
                monthly_earnings = place.rate * place.occupancy
                self.profits += monthly_earnings
    
    def make_bids(self):
        
        bids = []
        
        # Identify all neighboring listings (opportunities) that are adjacent 
        # to any currently owned properties but not yet owned
        opportunities = set()
        
        for place_id in self.assets:
            # Get the Place object for this owned property
            place = self.city.get_place(place_id)
            if place is not None:
                # Add all neighbors that are not already owned
                for neighbor_id in place.neighbours:
                    if neighbor_id not in self.assets:
                        opportunities.add(neighbor_id)
        
        # For each opportunity, evaluate and potentially make a bid
        for opportunity_id in opportunities:
            opportunity_place = self.city.get_place(opportunity_id)
            if opportunity_place is None:
                continue
            
            # Get the current sale price (ask_price) from the property's price dictionary
            # Using the most recent entry
            if opportunity_place.price:
                ask_price = max(opportunity_place.price.values())
            else:
                continue  # Skip if no price history
            
            # If host's available profits are greater than or equal to asking price
            if self.profits >= ask_price:
                # Create a bid dictionary
                bid = {
                    'place_id': opportunity_id,
                    'seller_id': opportunity_place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits
                }
                bids.append(bid)
        
        return bids
    
    def make_bids_v02(self):
        
        bids = []
        
        # Identify all neighboring listings (opportunities) that are adjacent 
        # to any currently owned properties but not yet owned
        opportunities = set()
        
        for place_id in self.assets:
            # Get the Place object for this owned property
            place = self.city.get_place(place_id)
            if place is not None:
                # Add all neighbors that are not already owned
                for neighbor_id in place.neighbours:
                    if neighbor_id not in self.assets:
                        opportunities.add(neighbor_id)
        
        # For each opportunity, evaluate and potentially make a bid
        for opportunity_id in opportunities:
            opportunity_place = self.city.get_place(opportunity_id)
            if opportunity_place is None:
                continue
            
            # Get the current sale price (ask_price) from the property's price dictionary
            # Using the most recent entry
            if opportunity_place.price:
                ask_price = max(opportunity_place.price.values())
            else:
                continue  # Skip if no price history
            
            # If host's available profits are greater than or equal to asking price
            if self.profits >= ask_price:
                if getattr(self.city, "same_area_rule", False) and opportunity_place.area != self.area:
                    # Different area and rule is active → skip this opportunity
                    continue
                # Create a bid dictionary
                bid = {
                    'place_id': opportunity_id,
                    'seller_id': opportunity_place.host_id,
                    'buyer_id': self.host_id,
                    'spread': self.profits - ask_price,
                    'bid_price': self.profits
                }
                bids.append(bid)
        
        return bids
    
    def add_asset(self, place_id):
        
        self.assets.add(place_id)
    
    def remove_asset(self, place_id):
        
        self.assets.discard(place_id)
    
    def __str__(self):
        return f"Host(id={self.host_id}, area={self.area}, assets={len(self.assets)}, profits={self.profits:.2f})"
    
    def __repr__(self):
        return f"Host(host_id={self.host_id}, area={self.area}, assets={self.assets}, profits={self.profits:.2f})"