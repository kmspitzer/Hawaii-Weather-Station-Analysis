# sqlalchemy-challenge

# SQLalchemy Challenge
 
 ## Climate Analysis
 
       Kate Spitzer
       
       The SQLalchemy challenge uses precipitation and temperature observation data from several weather stations
       in Hawaii to facilitate our analysis.  Scripts were written using 3 Jupyter notebooks, and a Python file.
       
       Inputs:                                                  Outputs:
       -------                                                  --------
       -  Resources/hawaii.sqlite                               output/precip_barchart.png
       -  Resources/hawaii_measurement.csv                      output/temperature_histogram.png
       -  Resources/hawaii_stations.csv (not used)              output/trip_avgtemp_bar.png
                                                                output/dailynormals_area.png
 
       
       climate_analysis.ipynb:
       -----------------------
       
       This notebook creates a SQLalchemy connection to the hawaii.sqlite database, the table names are displayed and 
       inspect is used to examine the table columns and data types.
       
       The database is then reflected, references are created to each table, and a session is initiated.
       
       We were tasked to determine the most recent date that exists in the Measurement table, and use that to
       query the database for the most recent year's precipitation data.  The data is placed in a Pandas DataFrame,
       and a bar chart is generated showing precipitation measurements over the latest year of data, using the Pandas
       plot.bar() method.  It was necessary to reduce the number of tick labels shown on the x axis, as there were more
       than 2000 data points, making the labels unreadable.  The chart is saved as a PNG in the file
       output/precip_barchart.png.  Finally, summary statistics for the table are displayed.
       
       Next, we were to list the stations found in the Measurement table, along with the number of datapoints associated
       with each one, in descending order by number of datapoints.  Then we were to pull the station id for the most
       active station (station with the most datapoints), and use this to calculate the minimum, maximum and average
       temperature reported for that station.
       
       We then pulled the temperature observation (tobs) data for the most recent year from the Measurement table, stored
       it in a Pandas DataFrame, and used it to generate a histogram of temperature data using the Pandas plot.hist()
       method. The chart is saved as a PNG in the file output/temperature_histogram.png.
       
       Finally, our session was closed.
       
       app.py
       ------
       
       This script uses Flask to create a simple web application that has a few simple routes which access the hawaii.sqlite
       database.

       /api/v1.0/precipitation
           - returns a JSON dictionary of all precipitation data
               from the measurement table using date as the key
               and prcp as the value.
       /api/v1.0/stations
           - returns a JSON list of all stations found in the
               stations table.
       /api/v1.0/tobs
           - returns a JSON list of all temperature observation
               data found in the measurement table.
       /api/v1.0/start_date
           - returns a JSON list containing the minimum temperature,
               the average temperature, and the maximum temperature
               from the measurement table for all dates beginning
               at the start date entered and later.
       /api/v1.0/start_date/end_date
           - returns a JSON list containing the minimum temperature,
               the average temperature, and the maximum temperature
               from the measurement table for all dates between the
               start date and end date entered, inclusive.
              
       
       temp_analysis_bonus_1.ipynb:
       ----------------------------
       
       In this notebook, we are attempting to see if the average observed temperature in Hawaii in June differs
       statistically from the average observed temperature in December.
       We read the Hawaii data from hawaii_measurements.csv into a Pandas DataFrame, and converted the date column from
       a string to a datatime object.  The dataset was cleaned by dropping rows containing null data.  We then pulled all
       June datapoints into another DataFrame, and the December datapoints into a third DataFrame.
       
       The temperature data for June and December were then pulled into lists in preparation for our t-test.
       
       
       temp_analysis_bonus_2.ipynb:
       ----------------------------
       
       This notebook creates a SQLalchemy connection to the hawaii.sqlite database, the table names are displayed,
       the database is  reflected, references are created to each table, and a session is initiated.
       
       We chose a year with data in the Measurement table, and used the calc_temps() method provided to calculate
       the minimum, maximum and average temperatures measured in that year.  We then used those statistics to
       generate a single-bar bar chart with an error bar to indicate estimated error or uncertainty in the data.
       The chart is saved as a PNG in the file output/trip_avgtemp_bar.png.
       
       We then joined the Measurement and Station tables to calculate total precipitation measure per station,
       and display that data along with the station id, the station name, and the station's latitude, longitude,
       and elevation in ascending order by total precipitation.
       
       Next, we chose dates for a hypothetical trip to Hawaii.  We chose historical data to match those dates, and
       used the daily_normals() method provided to calculate the minimum, average and maximum temperature for those dates.
       We placed the calculated data in a Pandas DataFrame and used the dataframe to generate and area plot, using the
       Pandas plot.area() method. The chart is saved as a PNG in the file output/dailynormals_area.png. 
       
       Finally, our session was closed.

       
       
