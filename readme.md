## track my eye drops usage

Augentropen (eye drops)


### usage

add new datatime for current time
```
./at.py
```

with specific time and/or date
```
./at.py -t 18:17 -d 2021-09-17
```

show last entry
```
./at.py -l
```


### dataformat

- csv with 5 columns: date, time, timezone, dayname and date_rolling
- date_rolling is set to the previous day when time is before 5am
