import pandas as pd
from .place import Place
from .hosts import Host


class City:
    
    def __init__(self, size, area_rates):
        
        self.size = size
        self.area_rates = area_rates
        self.step = 0
        
        # Will be populated by initialize()
        self.places = []
        self.hosts = []
        
        # Dictionary for quick place lookup by ID
        self._place_dict = {}
        
        # Initialize the city
        self.initialize()
    
    def initialize(self):
        
        # Generate Place instances for each grid cell
        place_id = 0
        for row in range(self.size):
            for col in range(self.size):
                # Create place with unique ID and initial host ID (same as place ID)
                place = Place(place_id=place_id, host_id=place_id, city=self)
                
                # Set up neighbors based on grid position
                self._setup_neighbors(place, row, col)
                
                # Add to places list and lookup dictionary
                self.places.append(place)
                self._place_dict[place_id] = place
                
                place_id += 1
        
        # Create Host instances - one for each place as initial owner
        for place in self.places:
            host = Host(host_id=place.host_id, place=place, city=self)
            self.hosts.append(host)
    
    def _setup_neighbors(self, place, row, col):
        
        neighbors = []
        
        # Check all 8 surrounding cells (unless on border)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the place itself
                    continue
                
                new_row, new_col = row + dr, col + dc
                
                # Check if neighbor is within grid bounds
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    neighbor_id = new_row * self.size + new_col
                    neighbors.append(neighbor_id)
        
        place.neighbours = neighbors
    
    def get_place(self, place_id):
        
        return self._place_dict.get(place_id)
    
    def get_area_mean_rate(self, area):
        
        if area in self.area_rates:
            rate_min, rate_max = self.area_rates[area]
            return (rate_min + rate_max) / 2
        return 125  # Default fallback
    
    def approve_bids(self, bids):
        
        if not bids:
            return []
        
        # Convert bids to pandas DataFrame and sort by spread in descending order
        df_bids = pd.DataFrame(bids)
        df_bids = df_bids.sort_values('spread', ascending=False)
        
        approved_transactions = []
        buyers_used = set()  # Track buyers who have already made a purchase
        places_sold = set()  # Track places that have already been sold
        
        # Evaluate each bid (most competitive first)
        for _, bid in df_bids.iterrows():
            buyer_id = bid['buyer_id']
            place_id = bid['place_id']
            
            # Check if both buyer and property are still available
            if buyer_id not in buyers_used and place_id not in places_sold:
                # Approve the transaction
                approved_transactions.append(bid.to_dict())
                buyers_used.add(buyer_id)
                places_sold.add(place_id)
        
        return approved_transactions
    
    def execute_transactions(self, transactions):
        
        executed_transactions = []
        
        for transaction in transactions:
            buyer_id = transaction['buyer_id']
            seller_id = transaction['seller_id']
            place_id = transaction['place_id']
            bid_price = transaction['bid_price']
            
            # Find buyer and seller hosts
            buyer_host = None
            seller_host = None
            
            for host in self.hosts:
                if host.host_id == buyer_id:
                    buyer_host = host
                elif host.host_id == seller_id:
                    seller_host = host
            
            if buyer_host is None or seller_host is None:
                continue  # Skip if hosts not found
            
            # Get the place object
            place = self.get_place(place_id)
            if place is None:
                continue  # Skip if place not found
            
            # Execute the transaction
            # Buyer pays the bid price and gains the property
            buyer_host.profits -= bid_price
            buyer_host.add_asset(place_id)
            
            # Seller receives the payment and loses the asset
            seller_host.profits += bid_price
            seller_host.remove_asset(place_id)
            
            # Update the place's host_id and record price history
            place.host_id = buyer_id
            place.price[self.step] = bid_price
            
            executed_transactions.append(transaction)
        
        return executed_transactions
    
    def clear_market(self):
        
        # Collect all bids from hosts
        all_bids = []
        for host in self.hosts:
            # Use make_bids_v02 if same_area_rule is enabled
            if self.same_area_rule:
                host_bids = host.make_bids_v02()
            else:
                host_bids = host.make_bids()
            all_bids.extend(host_bids)
        
        # Approve bids
        approved_transactions = self.approve_bids(all_bids)
        
        # Execute approved transactions
        executed_transactions = []
        if approved_transactions:
            executed_transactions = self.execute_transactions(approved_transactions)
        
        return executed_transactions
    
    def iterate(self):
        
        # Increase the step counter
        self.step += 1
        
        # Update occupancy for every place
        for place in self.places:
            place.update_occupancy()
        
        # Update profits for every host
        for host in self.hosts:
            host.update_profits()
        
        # Process transactions for this period and return the resulting list
        transactions = self.clear_market()
        
        return transactions
    
    def __str__(self):
        return f"City(size={self.size}, step={self.step}, places={len(self.places)}, hosts={len(self.hosts)})"
    
    def __repr__(self):
        return f"City(size={self.size}, step={self.step}, places={len(self.places)}, hosts={len(self.hosts)}, area_rates={self.area_rates})"