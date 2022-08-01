#!/usr/bin/env python
# coding: utf-8


import  pandas      as pd
import  requests
import  calendar
import  json

from    sqlalchemy  import create_engine
from    bs4         import BeautifulSoup
import  configparser


#
# Reading configuration file for passwords.


config = configparser.ConfigParser()
config.read('../my_config.ini')
 
# get all the connections
config.sections()
DBPass = config.get('postgres', 'password')
FlightKey = config.get('FlightLabs', 'mykey')


#
# START OF AIRPORTS FILE

print("10 Airport data extraction started...")

airport_file = "Resources/list-of-airports-in-australia-hxl-tags-1.csv"
airport_df = pd.read_csv(airport_file,skiprows=[1])
formatted_airport_df = airport_df[['id', 'ident', 'type','name','latitude_deg','longitude_deg','iso_region','municipality','gps_code','iata_code','score']].copy()


#Rename columns
rename_dict = {'latitude_deg':'latitude',
               'longitude_deg':'longitude',
               'iso_region':'region'}

formatted_airport_df.rename(columns = rename_dict, inplace = True)

#Process Region
formatted_airport_df['region'] = formatted_airport_df['region'].str[3:9]



#
# START OF ROUTES/TRAFFIC FILE
print("20 Airport traffic extraction started...")

airport_traffic = "Resources/TopRoutesJuly2014May2022.xlsx"

range1 = [i for i in range(0,11)]
range2 = [i for i in range(12,15)]
range3 = [i for i in range(16,19)]
range4 = [i for i in range(20,21)]

usecols = range1 + range2 + range3 + range4
skiprows = [i for i in range(1,13)]


#airport_traffic_df = pd.read_excel(airport_traffic, sheet_name='Top Routes',skiprows=[1,2,3,4,5,6,7,8,9,10,11,12],header=[1],usecols=usecols)
airport_traffic_df = pd.read_excel(airport_traffic, sheet_name='Top Routes',skiprows=skiprows,header=[1],usecols=usecols)

rename_dict = {}
#Rename columns
rename_dict = {airport_traffic_df.columns[1]:'Airport_Code_1',
               airport_traffic_df.columns[0]:'Airport_Code_0',
               airport_traffic_df.columns[2]:'Year',
               airport_traffic_df.columns[3]:'Month',
               airport_traffic_df.columns[4]:'Revenue_Passenger', 
               airport_traffic_df.columns[5]:'Aircraft_Trips',
               airport_traffic_df.columns[6]:'Rev_Pax_LF_Perc',
               airport_traffic_df.columns[7]:'Distance_klm',
               airport_traffic_df.columns[8]:'RPKs',
               airport_traffic_df.columns[9]:'ASKs',
               airport_traffic_df.columns[10]:'Seats',
               airport_traffic_df.columns[11]:'Annual_Revenue_Passenger', 
               airport_traffic_df.columns[12]:'Annual_Aircraft_Trips',
               airport_traffic_df.columns[13]:'Annual_Rev_Pax_LF_Perc',
               airport_traffic_df.columns[14]:'Annual_RPKs',
               airport_traffic_df.columns[15]:'Annual_ASKs',
               airport_traffic_df.columns[16]:'Annual_Seats',
               airport_traffic_df.columns[17]:'City_Pair_Route'
}

airport_traffic_df.rename(columns = rename_dict, inplace = True)

airport_traffic_df = airport_traffic_df.dropna()

dtypes_list = {}
dtypes_list = {"Aircraft_Trips":'int',
               "Distance_klm":'int',
               "RPKs":'int', 
               "ASKs":'int', 
               "Seats":'int', 
               "Annual_Aircraft_Trips":'int',
               "Annual_RPKs":'int',
               "Annual_ASKs":'int',
               "Annual_Seats":'int'
               }


airport_traffic_df = airport_traffic_df.astype(dtypes_list) 


#Format the Month name
airport_traffic_df['MM']    = airport_traffic_df['Month'] 
airport_traffic_df['Month'] = airport_traffic_df['Month'].apply(lambda x: calendar.month_abbr[x])

#
# START OF CITIES FILE
print("30 City extraction started...")

World_city_file = "Resources/World Cities.json"
world_city_df = pd.read_json(World_city_file)


au_city_df                  = world_city_df[(world_city_df.iso2 == "AU")].reset_index(drop=True)
au_city_df['city']          = au_city_df['city'].str.upper() 
au_city_df.rename(columns   = {'admin_name':'state'}, inplace = True)


#
# START OF STATES FILE
print("40 State extraction started...")

wikiurl="https://en.wikipedia.org/wiki/States_and_territories_of_Australia"

table_class="wikitable sortable" #From the page inspect

response = requests.get(wikiurl)
soup     = BeautifulSoup(response.text, 'html.parser')

indiatable  = soup.find_all('table',{'class':"wikitable sortable"})
states_list = pd.read_html(str(indiatable))

#First Table in the Wiki (Internal states)
#(states_list[0])

#Second Table in the Wiki (external states and territories)
#(states_list[1])


states_au_df = pd.DataFrame(states_list[0])
states_au_df = states_au_df[['State','Postal','Capital','Population(Dec 2021)[6]', 'Area (km2)[7]']]
states_au_df.rename(columns = {'State':'State_or_Territory'}, inplace = True)


states_external = pd.DataFrame(states_list[1])
states_external = pd.DataFrame(states_list[1])
states_external = states_external[['Territory','Postal','Capital(or largest settlement)','Population(Dec 2021)[6]', 'Area (km2)[7]']]
states_external.rename(columns = {'Territory':'State_or_Territory', 'Capital(or largest settlement)':'Capital'}, inplace = True)

formatted_states_df = pd.merge(states_au_df,states_external, how ='outer' )
formatted_states_df.rename(columns = {'Postal':'state_code','Population(Dec 2021)[6]':'Population_Dec_2021', 'Area (km2)[7]':'Area_km2'}, inplace = True)


#
# JOINING CITY with STATES. (replacing state code with state name field to keep the data unified.)

au_city_df = pd.merge(au_city_df, formatted_states_df, left_on=['state'], right_on=['State_or_Territory'] ) #, how="outer")

formatted_city_df = au_city_df[['city','lat','lng','state_code','population']]


#
# FATALITIES.
print("50 Fatalities extraction started...")

roads_file = "Resources/ardd_fatalities_jun2022.xlsx"

skiprows = [i for i in range(0,4)]

roads_file_df = pd.read_excel(roads_file, sheet_name='BITRE_Fatality',skiprows=skiprows)
roads_file_df.rename(columns = {'Heavy Rigid Truck Involvement':'Heavy Rigid Truck Inv', 'Articulated Truck Involvement':'Articulated Truck Inv'}, inplace = True)

roads_file_df['MM']    = roads_file_df['Month'] 
roads_file_df['Month'] = roads_file_df['Month'].apply(lambda x: calendar.month_abbr[x])
roads_file_df['State'] = roads_file_df['State'].str.upper() 


# 
# FLIGHT DATA

print("60 Flight extraction started...")

list_airport_df = formatted_airport_df[(formatted_airport_df.type == 'large_airport') ] 

flight_Date = []

departure_iata  = []
dept_terminal   = []
dept_gate       = []
delay           = []
dept_scheduled  = []

arr_iata        = []
arr_terminal    = []
arr_gate        = []
arr_baggage     = []
airline         = []
airline_iata    = []
flight_iata     = []


base_url = "https://app.goflightlabs.com/flights?"
for index, row in list_airport_df.iterrows(): 
    #continue  


    query_url = f"{base_url}access_key={FlightKey}&flight_status=active&dep_iata={row.iata_code}"


    try:
            response = requests.get(query_url)   
            places_data = response.json()


            if response.status_code == 200:


                for a in places_data:

                    flight_Date.append(a['flight_date'])
                    departure_iata.append(a['departure']['iata'])
                    dept_terminal.append(a['departure']['terminal'])
                    dept_gate.append(a['departure']['gate'])
                    delay.append(a['departure']['delay'])
                    dept_scheduled.append(a['departure']['scheduled'])

                    arr_iata.append(a['arrival']['iata'])
                    arr_terminal.append(a['arrival']['terminal'])
                    arr_gate.append(a['arrival']['gate'])
                    arr_baggage.append(a['arrival']['baggage'])
                    airline.append(a['airline']['name'])
                    airline_iata.append(a['airline']['iata'])
                    flight_iata.append(a['flight']['iata'])


    except KeyError:
        print(f"Unexpected Error calling API") 


flight_df = pd.DataFrame({            
                        'flight_Date':flight_Date,            
                        'departure_iata':departure_iata,
                        'dept_terminal':dept_terminal,             
                        'dept_gate': dept_gate,
                        'delay':delay,

                        'arr_iata':arr_iata,            
                        'arr_terminal':arr_terminal,
                        'arr_gate':arr_gate,             
                        'arr_baggage': arr_baggage,

                        'airline':airline,            
                        'airline_iata':airline_iata,
                        'flight_iata':flight_iata             
                    })


#
# LOADING DATAFRAMES TO DATABASE.

print("70 Database load started...")

rds_connection_string = f"postgres:{DBPass}@localhost:5432/project2"
engine = create_engine(f'postgresql://{rds_connection_string}')

# 1- City
formatted_city_df.to_sql(name='city', con=engine, if_exists='replace', index=False)

# 2- Airport
formatted_airport_df.to_sql(name='airports', con=engine, if_exists='replace', index=False)

# 3- Airport Routes / Traffic
airport_traffic_df.to_sql(name='airport_traffic', con=engine, if_exists='replace', index=False)

# 4- States
formatted_states_df.to_sql(name='states', con=engine, if_exists='replace', index=False)

# 5- Fatalities
roads_file_df.to_sql(name='road_fatalities', con=engine, if_exists='replace', index=False)

# 6- Flights
flight_df.to_sql(name='flights', con=engine, if_exists='append', index=False)

print("80 Program completed successfully...")