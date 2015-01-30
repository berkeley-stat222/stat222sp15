# http://stat-computing.org/dataexpo/2009/the-data.html
# 1987 - 2008
BASEURL="http://stat-computing.org/dataexpo/2009"
#for YEAR in $(seq 2006 2008)
#do
#    wget ${BASEURL}/${YEAR}.csv.bz2
#    bunzip2 ${YEAR}.csv.bz2
#done

#wget http://stat-computing.org/dataexpo/2009/*.csv.bz2

sqlite3 ontime.sqlite3 <<SQL
create table ontime (
  Year int,
  Month int,
  DayofMonth int,
  DayOfWeek int,
  DepTime  int,
  CRSDepTime int,
  ArrTime int,
  CRSArrTime int,
  UniqueCarrier varchar(5),
  FlightNum int,
  TailNum varchar(8),
  ActualElapsedTime int,
  CRSElapsedTime int,
  AirTime int,
  ArrDelay int,
  DepDelay int,
  Origin varchar(3),
  Dest varchar(3),
  Distance int,
  TaxiIn int,
  TaxiOut int,
  Cancelled int,
  CancellationCode varchar(1),
  Diverted varchar(1),
  CarrierDelay int,
  WeatherDelay int,
  NASDelay int,
  SecurityDelay int,
  LateAircraftDelay int
);

SQL

#for YEAR in $(seq 2006 2008)
#do
sqlite3 ontime.sqlite3 <<SQL
.separator ,
.import 2006.csv ontime
SQL
#done

sqlite3 ontime.sqlite3 <<SQL
delete from ontime where typeof(year) == "text";

create index year on ontime(year);
create index date on ontime(year, month, dayofmonth);
create index origin on ontime(origin);
create index dest on ontime(dest);
SQL
