import random
import matplotlib.pyplot as plt
import numpy as np
import os
from src.city import City


def set_random_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)


def calculate_host_wealth(host, city):
    
    wealth = host.profits
    
    # Add the most recent sale price of all owned properties
    for place_id in host.assets:
        place = city.get_place(place_id)
        if place and place.price:
            # Get the most recent price (highest step number)
            most_recent_price = max(place.price.values())
            wealth += most_recent_price
    
    return wealth


def run_simulation():

    # Set random seed for reproducible results
    set_random_seed(42)
    
    # Define simulation parameters
    city_size = 10
    area_rates = {
        0: (100, 200),  # bottom-left
        1: (50, 250),   # bottom-right  
        2: (250, 350),  # top-left
        3: (150, 450)   # top-right
    }
    
    # Create city
    print("Initializing city...")
    city = City(size=city_size, area_rates=area_rates)
    print(f"City created with {len(city.places)} places and {len(city.hosts)} hosts")
    
    # Run simulation for 15 years (180 monthly steps)
    total_steps = 180
    print(f"Running simulation for {total_steps} steps...")
    
    all_transactions = []
    
    for step in range(total_steps):
        transactions = city.iterate()
        all_transactions.extend(transactions)
        
        if (step + 1) % 12 == 0:  # Print progress every year
            year = (step + 1) // 12
            print(f"Year {year} completed. Total transactions so far: {len(all_transactions)}")
    
    print(f"Simulation completed. Total transactions: {len(all_transactions)}")
    
    return city, all_transactions


def create_wealth_chart(city):
    # Calculate wealth for each host
    host_data = []
    
    for host in city.hosts:
        wealth = calculate_host_wealth(host, city)
        host_data.append({
            'host_id': host.host_id,
            'wealth': wealth,
            'area': host.area
        })
    
    # Sort by wealth (smallest to largest)
    host_data.sort(key=lambda x: x['wealth'])
    
    # Prepare data for plotting
    wealths = [data['wealth'] for data in host_data]
    areas = [data['area'] for data in host_data]
    
    # Create color map for areas
    area_colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'orange'}
    colors = [area_colors[area] for area in areas]
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(wealths)), wealths, color=colors)
    
    plt.xlabel('Host (sorted by wealth)')
    plt.ylabel('Total Wealth')
    plt.title('Host Wealth Distribution by Area of Origin')
    
    # Create legend
    legend_elements = [plt.Rectangle((0,0),1,1, color=area_colors[i], 
                                   label=f'Area {i}') for i in range(4)]
    plt.legend(handles=legend_elements, loc='upper left')
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig('reports/graph1.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Wealth distribution chart saved as reports/graph1.png")
    
    return host_data


def create_additional_analysis(city, host_data):

    # Calculate average wealth by area
    area_wealth = {0: [], 1: [], 2: [], 3: []}
    
    for data in host_data:
        area_wealth[data['area']].append(data['wealth'])
    
    # Calculate statistics by area
    area_stats = {}
    for area in range(4):
        if area_wealth[area]:
            area_stats[area] = {
                'mean': np.mean(area_wealth[area]),
                'median': np.median(area_wealth[area]),
                'std': np.std(area_wealth[area]),
                'count': len(area_wealth[area])
            }
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Chart 1: Average wealth by area
    areas = list(area_stats.keys())
    means = [area_stats[area]['mean'] for area in areas]
    area_colors = ['red', 'blue', 'green', 'orange']
    
    ax1.bar(areas, means, color=area_colors)
    ax1.set_xlabel('Area')
    ax1.set_ylabel('Average Wealth')
    ax1.set_title('Average Wealth by Area')
    ax1.set_xticks(areas)
    
    # Chart 2: Wealth distribution (box plot style)
    wealth_by_area = [area_wealth[area] for area in areas]
    bp = ax2.boxplot(wealth_by_area, labels=areas, patch_artist=True)
    
    for patch, color in zip(bp['boxes'], area_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_xlabel('Area')
    ax2.set_ylabel('Wealth Distribution')
    ax2.set_title('Wealth Distribution by Area')
    
    plt.tight_layout()
    plt.savefig('reports/graph2_v0.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Additional analysis saved as reports/graph2_v0.png")
    
    # Print some interesting statistics
    print("\n=== SIMULATION RESULTS ===")
    print(f"Total hosts: {len(host_data)}")
    print(f"Simulation steps: {city.step}")
    
    print("\nWealth statistics by area:")
    for area in range(4):
        if area in area_stats:
            stats = area_stats[area]
            rate_range = city.area_rates[area]
            print(f"Area {area} (rate range {rate_range}): "
                  f"avg={stats['mean']:.0f}, "
                  f"median={stats['median']:.0f}, "
                  f"hosts={stats['count']}")


def main():
    
    print("Starting Airbnb Market Simulation")
    print("=" * 40)
    
    # Run the simulation
    city, transactions = run_simulation()
    
    # Create wealth distribution chart
    host_data = create_wealth_chart(city)
    
    # Create additional analysis
    create_additional_analysis(city, host_data)
    
    print("\n" + "=" * 40)
    print("Simulation completed successfully!")
    print("Check the 'reports' folder for generated graphs.")


if __name__ == "__main__":
    main()