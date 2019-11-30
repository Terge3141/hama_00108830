# Hama wireless socket 00108830
A very simple sender for hama 00108830 wireless socket written in python

## Setup
Connect as shown in the picture
DATA to GPIO17 (default)

![Wiring](wiring.png)

## Run script
```
./hamasender.py <buttonnr> <on|off>
```

for example
```
./hamasender.py 1 on
```
or
```
./hamasender.py all off
```
