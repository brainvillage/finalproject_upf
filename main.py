import random
import matplotlib.pyplot as plt
import numpy as np
import os
from src.city import City


def set_random_seed(seed=42):
    """Set random seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)


def calculate_host_wealth(host, city):
    """Calculate total wealth = profits + most recent property prices"""
    wealth = host.profits
    
    # Add the most recent sale price of all owned properties
    for place_id in host.assets:
        place = city.get_place(place_id)
        if place and place.price:
            # Get the most recent price
            most_recent_price = max(place.price.values())
            wealth += most_recent_price
    
    return wealth


def run_simulation(area_rates, bidding_version='v0', num_steps=180, seed=42):
    """
    Run the simulation with specified bidding mechanism.
    """
    set_random_seed(seed)
    
    city = City(size=10, area_rates=area_rates)
    city.same_area_rule = (bidding_version == 'v02')
    
    for step in range(num_steps):
        city.iterate()
    
    return city


def create_wealth_chart(city, filename):
    """
    Create vertical bar chart sorted by wealth.
    Each bar = one host, height = wealth, color = area of origin
    """
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
    area_colors = {0: '#E74C3C', 1: '#3498DB', 2: '#2ECC71', 3: '#F39C12'}
    colors = [area_colors[area] for area in areas]
    
    # Create the plot
    plt.figure(figsize=(14, 6))
    plt.bar(range(len(wealths)), wealths, color=colors, edgecolor='black', linewidth=0.5)
    
    plt.xlabel('Host (sorted by wealth)', fontsize=12)
    plt.ylabel('Total Wealth ($)', fontsize=12)
    plt.title('Host Wealth Distribution by Area of Origin', fontsize=14, fontweight='bold')
    
    # Create legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=area_colors[i], 
                                   edgecolor='black', label=f'Area {i}') for i in range(4)]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=11)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Save the chart
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved: {filename}")
    
    return host_data


def create_comparison_analysis(city, host_data, filename):
    """
    Create box plot comparing wealth distribution by area
    """
    # Group wealth by area
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
    area_colors_list = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']
    
    ax1.bar(areas, means, color=area_colors_list, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Area', fontsize=12)
    ax1.set_ylabel('Average Wealth ($)', fontsize=12)
    ax1.set_title('Average Wealth by Area', fontsize=13, fontweight='bold')
    ax1.set_xticks(areas)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Chart 2: Wealth distribution (box plot)
    wealth_by_area = [area_wealth[area] for area in areas]
    bp = ax2.boxplot(wealth_by_area, labels=[f'Area {a}' for a in areas], 
                     patch_artist=True, widths=0.6)
    
    for patch, color in zip(bp['boxes'], area_colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
    
    ax2.set_xlabel('Area', fontsize=12)
    ax2.set_ylabel('Wealth Distribution ($)', fontsize=12)
    ax2.set_title('Wealth Distribution by Area', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Analysis saved: {filename}")
    
    # Print statistics
    print(f"\nWealth statistics by area:")
    for area in range(4):
        if area in area_stats:
            stats = area_stats[area]
            rate_range = city.area_rates[area]
            print(f"  Area {area} (rate range {rate_range}): "
                  f"avg=${stats['mean']:.0f}, "
                  f"median=${stats['median']:.0f}, "
                  f"hosts={stats['count']}")


def main():
    
    print("=" * 60)
    print("Starting Airbnb Market Simulation")
    print("=" * 60)
    
    # Define area rates as specified
    area_rates = {
        0: (100, 200),
        1: (50, 250),
        2: (250, 350),
        3: (150, 450)
    }
    
    print(f"\nSimulation parameters:")
    print(f"  City size: 10×10")
    print(f"  Steps: 180 (15 years)")
    print(f"  Area rates: {area_rates}")
    print(f"  Seed: 42 (for reproducibility)")
    
    # Run v0 (original make_bids - no area restriction)
    print("\n" + "-" * 60)
    print("Running Simulation v0 (No area restriction)...")
    print("-" * 60)
    city_v0 = run_simulation(area_rates, bidding_version='v0', num_steps=180, seed=42)
    host_data_v0 = create_wealth_chart(city_v0, 'reports/graph1.png')
    create_comparison_analysis(city_v0, host_data_v0, 'reports/graph2_v0.png')
    
    # Run v02 (make_bids_v02 with area restriction)
    print("\n" + "-" * 60)
    print("Running Simulation v02 (With area restriction)...")
    print("-" * 60)
    city_v02 = run_simulation(area_rates, bidding_version='v02', num_steps=180, seed=42)
    host_data_v02 = create_wealth_chart(city_v02, 'reports/graph1_v02.png')
    create_comparison_analysis(city_v02, host_data_v02, 'reports/graph2_v02.png')
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total hosts: {len(host_data_v0)}")
    print(f"Total simulation steps: {city_v0.step}")
    
    print("\n" + "=" * 60)
    print("✓ All graphs saved to reports/ folder:")
    print("  - graph1.png (wealth by host, v0)")
    print("  - graph2_v0.png (area comparison, v0)")
    print("  - graph1_v02.png (wealth by host, v02)")
    print("  - graph2_v02.png (area comparison, v02)")
    print("=" * 60)


if __name__ == "__main__":
    main()
