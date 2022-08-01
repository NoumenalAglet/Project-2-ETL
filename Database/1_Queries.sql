select  
         ap."region",
         ap."name" as STarting_Airport,
         "Year",
         "Month",
         sum("Aircraft_Trips") Sum_Aircraft_trips,
         sum("Revenue_Passenger") Sum_Revenue_Passengers
  from airport_traffic air_trf
  join  airports ap on air_trf."Airport_Code_0" = ap.iata_code
  Where "Year" = '2022'
  Group By ap."name",
         ap."region",
         "Year",
         "Month",
         air_trf."MM"
Order By 1,2,3,air_trf."MM"


select  "State",
         "Year",
         "Month",
         count(*)
  From road_fatalities
 Where "Year" In ('2021', '2022' )
Group By "State",
         "Year",
         "Month",
         "MM"
Order By 1,2,"MM"
         
        

-- Airport Counts By State and Type
select stt."State_or_Territory",
       stt."state_code",
       stt."Population_Dec_2021",
       stt."Area_km2",
       ap."type",
       Count(ap.id) Airport_Count
  from states stt
 left join airports ap on (stt."state_code" = ap."region") 
Group By stt."State_or_Territory",
         stt."state_code" ,
         stt."Population_Dec_2021",
         stt."Area_km2",
         ap."type"
Order By stt."State_or_Territory",ap."type"
         
         
-- Airport Counts By State and Type
select stt."State_or_Territory",
       stt."state_code",
       stt."Population_Dec_2021",
       stt."Area_km2",
       ap."type",
       Count(ap.id) Airport_Count,
       sum("Aircraft_Trips") Sum_Aircraft_trips,
       sum("Revenue_Passenger") Sum_Revenue_Passengers
  from states stt
 left join airports ap on (stt."state_code" = ap."region")
 left join airport_traffic ap_trf on (ap.iata_code = ap_trf."Airport_Code_0" and "Year" = '2021')
Group By stt."State_or_Territory",
         stt."state_code" ,
         stt."Population_Dec_2021",
         stt."Area_km2",
         ap."type"
Order By stt."State_or_Territory",ap."type"
  
  