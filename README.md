# covid-ca
covid-ca is an application that pulls COVID-19 data together from the provinces and territories of Canada for storage in a database and exposure via JSON and visualizations. 

Currently the application grabs, stores and exposes a JSON representation of daily COVID-19 summary data from the province of Ontario

#### Dependencies

- Python 3.6+
- Postgresql

#### Installation

1. Clone repo
2. Set up python environment
	- Set up python virtual environment
		- ```python3 -m venv venv-covid-ca```
		- ```source venv-covid-ca/bin/activate```
	- Install requirements
		- ```pip install -r requirements.txt```
3. Start database server
	 - ```brew services start postgres```
	 - ```createdb covid-ca```
4. Set up application environment
	- ```cp example.env .env```
	- change ```DATABASE_URL``` in .env to match your connection information
5. Seed data
	- Pull data for the first time
		- ```foreman run scraper.py```
	- Run web server
		- ```foreman start```
	- View `http://localhost:5000/ontario.json` in browser to test. You should see a JSON representation of daily updates from Ontario