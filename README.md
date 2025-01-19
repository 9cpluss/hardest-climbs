Feel free to use the data in this repository but please credit the website [hardestclimbs.com](https://www.hardestclimbs.com).
If you spot a mistake or would like to add some data, please create a new issue or create a pull request.

# Data Structure

The data is structured as a relational group of three csvs: 
* climbers_table
* route_table
* sends table

## climbers_table.csv
Contains basic biographical information about climbers.

| Column Name    | Data Type | Description                           | Example   |
|---------------|-----------|---------------------------------------|-----------|
| climber_id    | string    | Unique identifier for each climber    | cl00001   |
| first_name    | string    | Climber's first name                  | Adam      |
| last_name     | string    | Climber's last name                   | Ondra     |
| country       | string    | Country of origin (lowercase)         | czechia   |
| gender        | string    | Gender (male/female)                  | male      |
| year_of_birth | integer   | Year the climber was born            | 1993      |

- CSV file with header row
- Fields are comma-separated
- No quoted fields
- String values are case-sensitive
- Climber IDs follow the pattern 'cl' followed by 5 digits

## routes_table.csv
Contains detailed information about climbing routes.

| Column Name | Data Type | Description                          | Example    |
|------------|-----------|--------------------------------------|------------|
| route_name | string    | Name of the climbing route           | Silence    |
| type       | string    | Type of climbing (currently sport or boulder) | sport      |
| route_country    | string    | Country where route is located       | norway     |
| crag       | string    | Specific crag or climbing area       | Flatanger  |
| lat        | float     | Latitude coordinates                 | 64.489722  |
| long       | float     | Longitude coordinates                | 10.818611  |
| grade      | string    | Climbing grade of the route          | 9c         |
| route_id   | string    | Unique identifier for each route     | ro0001     |

- CSV file with header row
- Fields are comma-separated
- No quoted fields
- String values are case-sensitive
- Route IDs follow the pattern 'ro' followed by 4 digits
- Coordinates are in decimal degrees format
- Grade uses standard/european climbing grade notation

## sends_table.csv
Contains records of climbing ascents, linking climbers to specific routes.

| Column Name | Data Type | Description                                | Example    |
|------------|-----------|--------------------------------------------| ---------- |
| date       | date      | Date of the ascent (YYYY-MM-DD)           | 2024-01-01 |
| fa         | boolean   | First ascent flag (1 = FA, 0 = repeat)    | 1          |
| video      | string    | Video link if available (NA if none)      | NA         |
| climber_id | string    | Reference to climber in climbers.csv      | cl00043    |
| route_id   | string    | Reference to route in routes.csv          | ro0136     |

- CSV file with header row
- Fields are comma-separated
- Fields are quoted
- Date format is YYYY-MM-DD
- NA represents missing or not applicable data
- climber_id references climbers.csv (pattern: 'cl' + 5 digits)
- route_id references routes.csv (pattern: 'ro' + 4 digits)# Data Sources


# Sources:
Thanks to the following websites (not a complete list):
* 8a.nu
* climbing-history.org
* ukclimbing.com
* thecrag.com
* instagram
* youtube
