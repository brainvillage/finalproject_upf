# UPF Programming I final project

## Group Members
* jade.tilman@outlook.com | Jade Tilman. 
* joanhortalabas | Joan Hortalà i Bas. 
* jurigenthnerupf | Juri Genthner. 
* brainvillage | Tim Hirndorf. 

## Project Description
This project simulates an Airbnb-like booking system, analyzing real data from 2 cities (Barcelona and Berlin) and implements booking algorithms.

## Datasets
The datasets used in this analysis are sourced from Inside Airbnb webpage (http://insideairbnb.com/):

    - Barcelona, September: (http://data.insideairbnb.com/barcelona/2025-09-01/data/barcelona_sep_listings.csv.gz)
    - Berlin, September: (http://data.insideairbnb.com/berlin/2025-09-01/data/berlin_sep_listings.csv.gz)


Part 1:
- We based our work on the datasets from Barcelona and Berlin.
- Our main variables of interest were host_id and host_total_listings_count.
- We narrowed our scope to market concnetration.
- The graph reveals that there is a higher concentration in Barcelona than berlin.
Part 2:
- We would change the rule "bid" to avoid cross-market acquiitions.
- Our proposed graph illustrates that when limiting cross-market acquisition, concentration diminshed.
- This adjustment aims to avoid over concentration.
- In conclusion, we would change this rule because not all markets are the same and hosts are specilized.

## Project Structure
data/
notebooks/
└── part2.ipynb
reports/
├── graph1.png
├── graph2_v0.png
├── graph3.png
└── presentation.pdf
src/
└── final_project/
 ├── __init__.py
 ├── city.py
 ├── hosts.py
 └── place.py
main.py
pyproject.toml
README.md
uv.lock

