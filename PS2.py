#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('cd', '"C:/Users/11584/Desktop/OMGroup/ESE023"')
import os
# import pandas 
import pandas as pd
# import numpy
import numpy as np
# import matplotlib
from matplotlib import pyplot as plt
# make plots appear and be stored within the notebook
get_ipython().run_line_magic('matplotlib', 'inline')
os.getcwd()


# In[ ]:


##PS2_1_1

#met = pd.read_xlsx("earthquakes-2026-10-14_20-28-44_+0800.tsv")
Sig_Eqs = pd.read_csv("earthquakes-2026-10-14_20-28-44_+0800.tsv", sep = "\t")
Sig_Eqs1 = Sig_Eqs[['Deaths','Country']]
#print(Sig_Eqs1)
#Sig_Eqs2 = Sig_Eqs1.groupby(by = ['Country'], as_index=False).sum(min_count = 1).sort_values(['Deaths'], ascending = False)
#if not defined, every index will be sum
Sig_Eqs2 = Sig_Eqs1.groupby(by = ['Country'], as_index = False)['Deaths'].sum(min_count = 1).sort_values(['Deaths'], ascending = False)
#Sig_Eqs2.head(20)
Top_20 = Sig_Eqs2[0:20]
print(Top_20)


# In[ ]:


##PS2_1_2

Sig_Eqs1 = Sig_Eqs[['Ms','Year']]
large_eq = Sig_Eqs1.loc[ (Sig_Eqs1['Ms'] > 3) ]
eq_count = large_eq.groupby("Year").size()
#fill a zero into the year without a Sig_eq
last_year = int(Sig_Eqs["Year"].max())
years = range(-2150, last_year + 1)
eq_count = eq_count.reindex(years, fill_value=0)

plt.figure(figsize=(10, 4))
plt.plot(eq_count.index, eq_count.values)
plt.xlabel("Year (negative = BC)")
plt.ylabel("Number of recorded earthquakes")
plt.title("Significant earthquakes")
plt.grid(True)
plt.tight_layout()
plt.show()

#trend: 强地震记录在1500年开始逐年递增，
#到2000年达到最高峰，从2000年以后断崖式下跌.
#接下来分析原因：1500年以后，地震记录可能才开始完善，
#并且记录在后来才能有效保存，越接近古代，能得到保存的记录就越少


# In[ ]:


##PS2_1_2

Sig_Eqs1 = Sig_Eqs[['Ms', 'Year']]

#筛选2000年及以后的全部地震记录
total_eq = Sig_Eqs1.loc[Sig_Eqs1['Year'] >= 2000]

#在这些记录中筛选Ms>3的地震
large_eq = total_eq.loc[total_eq['Ms'] > 3]

#分别统计每年的次数
total_count = total_eq.groupby('Year').size()
large_count = large_eq.groupby('Year').size()

#补齐年份，没有符合条件记录的年份填 0
last_year = int(Sig_Eqs['Year'].max() )
years = range(2000, last_year + 1)

total_count = total_count.reindex(years, fill_value = 0 )
large_count = large_count.reindex(years, fill_value = 0 )

#连续调用两次 plot，将两条线画在同一张图上
plt.figure(figsize=(10, 4))
plt.plot(total_count.index, total_count.values, label = 'All records')
plt.plot(large_count.index, large_count.values, label = 'Ms > 3')

plt.xlabel('Year')
plt.ylabel( 'Number of recorded earthquakes')
plt.title('Significant earthquakes since 2000' )
plt.legend()
plt.grid( True )
plt.tight_layout()
plt.show()

#数据分析：自2014年开始，在总地震记录数目无显著下跌的情况下，
#强地震次数趋近于0.可能是强地震统计口径发生了变化


# In[ ]:


##PS2_1_3 definition
def CountEq_LargestEq(country):
    country_eq = Sig_Eqs[ Sig_Eqs[ "Country"]  == country]
    total = len(country_eq)

    #delete countries without records
    known_eq = country_eq.dropna(subset=["Mag"])
    if len(known_eq) == 0:
        return total, np.nan, np.nan, np.nan, np.nan, "Unknown"
    if country == "TAIWAN":
        print("TAIWAN is a region of China with independent records.")

    largest_index = known_eq["Mag"].idxmax()
    largest = known_eq.loc[largest_index]
    magnitude = largest[ "Mag" ]
    year = largest["Year"]
    month = largest["Mo"]
    day = largest[ "Dy"]
    location = largest["Location Name"]
    return total, magnitude, year, month, day, location


# In[ ]:


##PS2_1_3
# get the country list
countries = Sig_Eqs["Country"].dropna().unique()
results = []
# loop for every country
for country in countries:
    total, magnitude, year, month, day, location = CountEq_LargestEq(country)
    results.append([country, total, magnitude, year, month, day, location])

columns = ["Country", "Total_frequency", "Max_Mag", "Year", "Month", "Day", "Location"]
country_results = pd.DataFrame(results, columns = columns)
# transfer date into integer
country_results["Year"] = country_results["Year"].astype("Int64")
country_results["Month"] = country_results["Month"].astype("Int64")
country_results["Day"] = country_results["Day"].astype("Int64")

country_results = country_results.sort_values("Total_frequency", ascending = False)
country_results = country_results.reset_index(drop = True)


print(country_results.to_string)


# In[ ]:


##PS2_2 data tidy
weather = pd.read_csv("data/Baoan_Weather_1998_2022.csv", low_memory = False)
weather1 = weather[['DATE','TMP']]
temperatures = []
quality_codes = []
# +0618,1 prior 5 code refer to TMP. the last code refer to quality code
for value in weather["TMP"]:
    temperature = int(value[:5])
    quality = value[6]
    temperatures.append(temperature)
    quality_codes.append(quality)

weather["Temperature"] = temperatures
weather["Quality"] = quality_codes

# transfer codes to temperature
weather = weather.dropna(subset=["Temperature"])
weather = weather[weather["Temperature"] != 9999]
weather = weather[weather["Quality"].isin(["0", "1", "4", "5", "9"])]
# 1,5: good quality; 0,4: limit check data; 9: pass if it's present
weather["Temperature"] = weather["Temperature"] / 10
weather = weather[weather["Temperature"] >= -93.2]
weather = weather[weather["Temperature"] <= 61.8]
# range definition from POS 88-92

same_time = weather.groupby("DATE")["Temperature"].mean()
same_time = same_time.reset_index()
# more than one record in the same time

# mean by hours
hours = []
for date in same_time["DATE"]:
    hours.append(date[:13])
# 1998-01-01T00
# 01234567890123. a 12-digits code
same_time["Hour"] = hours
hourly_temp = same_time.groupby("Hour")["Temperature"].mean()
hourly_temp = hourly_temp.reset_index()

# mean by months
months = []
for hour in hourly_temp["Hour"]:
    months.append(hour[:7])
# 1998-01-01T00
# 01234567890123. a 12-digits code
hourly_temp["Month"] = months
monthly_temp = hourly_temp.groupby("Month")["Temperature"].mean()

all_months = []
month_numbers = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
for year in range(1998, 2023):
    for month in month_numbers:
        all_months.append(str(year) + "-" + month)
monthly_temp = monthly_temp.reindex(all_months)

print("有效记录数：", len(weather))
print("最后一个有效观测时刻：", weather["DATE"].max())
print(monthly_temp.head(12))



# In[ ]:


##PS2_2 ploting

plt.figure(figsize=(10, 4))
plt.plot(monthly_temp.index, monthly_temp.values)

plt.xlabel("Time")
plt.ylabel("Monthly mean temperature (°C)")
plt.title("Baoan Airport monthly temperature, 1998-2022")
plt.show()

# trend analysis
# bar plotting with coldest and hottest month of every year
# the coldest month is mainly on January, 
# while the hottest month is on July or October
year_records = []
hot_count = [0] * 12
cold_count = [0] * 12

for year in range(1998, 2023):
    year_temp = monthly_temp[str(year) + "-01":str(year) + "-12"]
    year_temp = year_temp.dropna()
    highest = year_temp.max()
    lowest = year_temp.min()
    hot_months = []
    cold_months = []

    for date in year_temp.index:
        month = int(date[5:7])

        if year_temp[date] == highest:
            hot_months.append(month)
            if len(year_temp) == 12:
                hot_count[month - 1] = hot_count[month - 1] + 1

        if year_temp[date] == lowest:
            cold_months.append(month)
            if len(year_temp) == 12:
                cold_count[month - 1] = cold_count[month - 1] + 1

    year_records.append([year, hot_months, cold_months, highest, lowest,
                         len(year_temp), len(year_temp) == 12])

columns = ["Year", "Warmest_months", "Coldest_months", "Highest_monthly_mean_C",
           "Lowest_monthly_mean_C", "Valid_months", "Included_in_frequency"]
year_months = pd.DataFrame(year_records, columns=columns)
print(year_months.to_string(index=False))

frequency = pd.DataFrame()
frequency["Month"] = range(1, 13)
frequency["Warmest_count"] = hot_count
frequency["Coldest_count"] = cold_count
print(frequency.to_string(index=False))
hot_positions = []
cold_positions = []
for month in range(1, 13):
    hot_positions.append(month - 0.2)
    cold_positions.append(month + 0.2)

plt.figure(figsize=(10, 5))
plt.bar(hot_positions, hot_count, width=0.4, color="red", label="Warmest month")
plt.bar(cold_positions, cold_count, width=0.4, color="blue", label="Coldest month")
plt.xticks(range(1, 13))
plt.yticks(range(0, max(hot_count + cold_count) + 1))
plt.xlabel("Month")
plt.ylabel("Frequency (number of years)")
plt.title("Baoan: warmest and coldest months, 1998-2021")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()



# In[ ]:


##PS2_3_1 group the data, 10 largest hurricanes
columns = ["SID", "SEASON", "BASIN", "NAME", "ISO_TIME", "LAT", "LON", "WMO_WIND"]
df = pd.read_csv("data/ibtracs.ALL.list.v04r00.csv", usecols=columns,
                 skiprows=[1], dtype=str, keep_default_na=False)
for column in columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].replace("", np.nan)

df["NAME"] = df["NAME"].replace("NOT_NAMED", "Unnamed")
df["NAME"] = df["NAME"].fillna("Unnamed")
df["BASIN"] = df["BASIN"].fillna("Unknown")
df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"])
for column in ["SEASON", "LAT", "LON", "WMO_WIND"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df.loc[df["WMO_WIND"] < 0, "WMO_WIND"] = np.nan

print(df.head())
print("数据点数：", len(df))
print("最后一个观测时刻：", df["ISO_TIME"].max())
storm_wind = df.groupby("SID")["WMO_WIND"].max()
storm_name = df.groupby("SID")["NAME"].first()

# 两个 Series 都用 SID 作索引，会对应到同一个风暴
storms = pd.DataFrame()
storms["NAME"] = storm_name
storms["WMO_WIND"] = storm_wind
storms = storms.dropna(subset=["WMO_WIND"])
storms = storms.reset_index()
storms = storms.sort_values(["WMO_WIND", "SID"], ascending=[False, True])

print(storms.head(10))


# In[ ]:


##PS2_3_2 20 strongest hurricanes
top20_storms = storms.head(20)
print(top20_storms)


# In[ ]:


##PS2_3_3 basin count
basin_counts = df.groupby("BASIN").size()
basin_counts = basin_counts.sort_values(ascending=False)
print(basin_counts.to_frame("Datapoints"))
print("各海盆合计：", basin_counts.sum())


# In[ ]:


##PS2_3_4 Latitude and Longitude.
positions = df.dropna(subset=["LAT", "LON"])
positions = positions[(positions["LAT"] >= -90) & (positions["LAT"] <= 90)]
positions = positions[(positions["LON"] >= -180) & (positions["LON"] <= 180)]

plt.figure(figsize=(10, 5))
plt.hexbin(positions["LON"], positions["LAT"], gridsize=80, mincnt=1, bins="log")
plt.colorbar(label="Datapoints per hexagon (log scale)")
plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.title("IBTrACS track-point locations")
#plt.tight_layout()
plt.show()


# In[ ]:


##PS2_3_5 Typhoon Mangkhut
mangkhut = df[df["NAME"] == "MANGKHUT"]
mangkhut = mangkhut[mangkhut["SEASON"] == 2018]
mangkhut = mangkhut.sort_values("ISO_TIME")
mangkhut = mangkhut.dropna(subset=["LAT", "LON"])

plt.figure(figsize=(9, 5))
plt.plot(mangkhut["LON"], mangkhut["LAT"], "o-", markersize=3)
plt.plot(mangkhut["LON"].iloc[0], mangkhut["LAT"].iloc[0], "go", label="Initiation")
plt.plot(mangkhut["LON"].iloc[-1], mangkhut["LAT"].iloc[-1], "rx", label="Terminal")
plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.title("Typhoon Mangkhut, 2018")
plt.legend()
plt.grid(True)
#plt.tight_layout()
plt.show()


# In[ ]:


##PS2_3_6 WP to EP basin
pacific = df[df["ISO_TIME"] >= "1970-01-01"]
pacific = pacific[(pacific["BASIN"] == "WP") | (pacific["BASIN"] == "EP")]
pacific = pacific.copy()

print("筛选后的数据点数：", len(pacific))
print(pacific.head())


# In[ ]:


##PS2_3_7 the day of year 
pacific_time = pacific.set_index("ISO_TIME")
daily_count = pacific_time.resample("D").size()
dates = pd.date_range("1970-01-01", "2022-10-13", freq="D")
daily_count = daily_count.reindex(dates, fill_value=0)

daily = pd.DataFrame()
daily["Count"] = daily_count

plt.figure(figsize=(10, 4))
plt.plot(daily.index, daily["Count"], linewidth=0.6)
plt.xlabel("Date")
plt.ylabel("Datapoints per day")
plt.title("Daily track-point counts in WP and EP")
plt.tight_layout()
plt.show()
print(daily.head())



# In[ ]:


##PS2_3_8 climatology
daily["Day_of_year"] = daily.index.dayofyear
baseline = daily["1970":"2021"]
climatology = baseline.groupby("Day_of_year")["Count"].mean()

print(climatology.head(10).to_frame("Mean_count"))
print("气候态计数最大的日序号：", climatology.idxmax())

plt.figure(figsize=(10, 4))
plt.plot(climatology.index, climatology.values)
plt.xlabel("Day of year")
plt.ylabel("Mean datapoints per day")
plt.title("Daily count climatology, 1970-2021")
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


##PS2_3_9 anomaly of daily counts
normal_values = []
for day in daily["Day_of_year"]:
    normal = climatology.loc[day]
    normal_values.append(normal)

daily["Climatology"] = normal_values
daily["Anomaly"] = daily["Count"] - daily["Climatology"]
print(daily.head())

plt.figure(figsize=(10, 4))
plt.plot(daily.index, daily["Anomaly"], linewidth=0.6)
plt.axhline(0, color="black")
plt.xlabel("Date")
plt.ylabel("Daily count anomaly")
plt.title("Daily track-point anomalies in WP and EP")
plt.tight_layout()
plt.show()


# In[ ]:


##PS2_3_10 anomaly timeseries at annual resolution 
annual_anomaly = daily["Anomaly"].resample("YS").mean()
annual_anomaly = annual_anomaly["1970":"2021"]

plt.figure(figsize=(10, 4))
plt.bar(annual_anomaly.index.year, annual_anomaly.values)
plt.axhline(0, color="black")
plt.xlabel("Year")
plt.ylabel("Annual mean daily anomaly")
plt.title("Annual track-point anomalies, 1970-2021")
plt.tight_layout()
plt.show()

high_years = annual_anomaly.sort_values(ascending=False)
low_years = annual_anomaly.sort_values()
print("距平最高的五年：")
print(high_years.head(5).to_frame())
print("距平最低的五年：")
print(low_years.head(5).to_frame())



# In[ ]:


## PS2_4_1
## 全球温度距平数据集
global_data = pd.read_csv("data/global_temperature.csv", comment="#", dtype=str)
global_data["Date"] = pd.to_datetime(global_data["Date"], format="%Y%m", errors="coerce")
global_data["Anomaly"] = pd.to_numeric(global_data["Departure from Average"], errors="coerce")
global_data = global_data.dropna(subset=["Date", "Anomaly"])
global_data = global_data[global_data["Anomaly"] > -99]
global_data = global_data.drop_duplicates()
print("重复月份数：", global_data["Date"].duplicated().sum())
##数据集删除缺失、极端占位值、重复行。转换日期、数值
global_data = global_data.set_index("Date")
global_data = global_data.sort_index()
global_temp = global_data["Anomaly"]
months = pd.date_range("1880-01-01", "2025-12-01", freq="MS")
global_temp = global_temp.reindex(months)

print("有效月份数：", global_temp.count())
print("缺失月份数：", global_temp.isna().sum())
print(global_temp.head().to_frame())


# In[ ]:


## PS2_4_2 anomaly timeseries 
global_annual = global_temp.resample("YS").mean()

plt.figure(figsize=(10, 4))
plt.plot(global_temp.index, global_temp.values, linewidth=0.5, label="Monthly")
plt.plot(global_annual.index, global_annual.values, linewidth=1.5, label="Annual mean")
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Year")
plt.ylabel("Temperature anomaly (°C)")
plt.title("Global temperature anomaly, 1880-2025")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[66]:


## PS2_4_3 basic analysis of 7 indexes
number = global_temp.count()
average = global_temp.mean()
median = global_temp.median()
std = global_temp.std()
minimum = global_temp.min()
maximum = global_temp.max()
value_range = maximum - minimum

statistics = pd.DataFrame()
statistics["Statistic"] = ["Count", "Mean", "Median", "Std", "Minimum", "Maximum", "Range"]
statistics["Value"] = [number, average, median, std, minimum, maximum, value_range]
print(statistics)
print("最小值出现时间：", global_temp.idxmin())
print("最大值出现时间：", global_temp.idxmax())

early_mean = global_temp["1880":"1909"].mean()
recent_mean = global_temp["1996":"2025"].mean()
print("1880-1909 年平均距平：", round(early_mean, 3), "°C")
print("1996-2025 年平均距平：", round(recent_mean, 3), "°C")
print("后期减去前期：", round(recent_mean - early_mean, 3), "°C")


# In[ ]:




