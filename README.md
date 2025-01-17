Feel free to use the data in this repository but please credit the website [hardestclimbs.com](https://www.hardestclimbs.com)

If you spot a mistake or would like to add some data, please create a new issue or create a pull request.

# Data Structure

The data is structured as a relational group of three csvs: 
* climbers_table
* route_table
* sends table

## climbers_table.csv
Contains basic biographical information about climbers.

### Schema
| Column Name    | Data Type | Description                           | Example   |
|---------------|-----------|---------------------------------------|-----------|
| climber_id    | string    | Unique identifier for each climber    | cl00001   |
| first_name    | string    | Climber's first name                  | Adam      |
| last_name     | string    | Climber's last name                   | Ondra     |
| country       | string    | Country of origin (lowercase)         | czechia   |
| gender        | string    | Gender (male/female)                  | male      |
| year_of_birth | integer   | Year the climber was born            | 1993      |

### Data Format
- CSV file with header row
- Fields are comma-separated
- No quoted fields
- String values are case-sensitive
- Climber IDs follow the pattern 'cl' followed by 5 digits

## routes_table.csv
Contains detailed information about climbing routes.

#### Schema
| Column Name | Data Type | Description                          | Example    |
|------------|-----------|--------------------------------------|------------|
| route_name | string    | Name of the climbing route           | Silence    |
| type       | string    | Type of climbing (currently sport or boulder) | sport      |
| country    | string    | Country where route is located       | Norway     |
| crag       | string    | Specific crag or climbing area       | Flatanger  |
| lat        | float     | Latitude coordinates                 | 64.489722  |
| long       | float     | Longitude coordinates                | 10.818611  |
| grade      | string    | Climbing grade of the route          | 9c         |
| route_id   | string    | Unique identifier for each route     | ro0001     |

#### Data Format
- CSV file with header row
- Fields are comma-separated
- No quoted fields
- String values are case-sensitive
- Route IDs follow the pattern 'ro' followed by 4 digits
- Coordinates are in decimal degrees format
- Grade uses standard/european climbing grade notation



# Data Sources
Thanks to the following websites (not a complete list):
* 8a.nu
* climbing-history.org
* ukclimbing.com
* thecrag.com
