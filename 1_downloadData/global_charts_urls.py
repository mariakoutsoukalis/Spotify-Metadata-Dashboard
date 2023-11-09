from datetime import datetime, timedelta #Classes from datetime module for dates, times, and representing duration

class DateTimeFrame:
    end_date = datetime(day=2, month=11,
                    year=2023)  #Set to latest date (always one day ahead of what is on the site)
    date_pairs = []

    #Looping through date range of 52 weeks and appending dates to an empty list.
    for x in range(0, 52):
        week_start = end_date - timedelta(days=7)
        weekend = end_date.strftime("%Y-%m-%d") #converting date into string using string format time.
        week_start = week_start.strftime("%Y-%m-%d")
        date_string = f"{week_start}--{weekend}"
        date_pairs.append(date_string)
        end_date = end_date - timedelta(days=7)

    url = "https://charts.spotify.com/charts/view/regional-global-weekly/"
    #Looping through the dates in the date_pairs list adding the weekend date to the base url to generate urls.
    for d in date_pairs:
        #Converts the date string a splits it leaving the corresponding 'weekend'
        urls = f"{url}{d.split('--')[1]}"
        print (urls)