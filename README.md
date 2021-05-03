# cowin-availability-command-line
A command line utility to check the availability of vaccine slots

## Usage

```
python cowin-availability.py -h

usage: cowin-availability.py [-h] [-t {pin,district}] [-s STATE] [-d DISTRICT] [-a AGE_LIMIT] [-p PIN_CODE]

optional arguments:
  -h, --help            show this help message and exit
  -t {pin,district}, --search_type {pin,district}
                        The type of search to perform. You can either directly give a pincode or give a combination of state + district.
  -s STATE, --state STATE
                        The name of the state
  -d DISTRICT, --district DISTRICT
                        The name of the district
  -a AGE_LIMIT, --age_limit AGE_LIMIT
                        The age limit. Put as 18 for 18+ and 45 for 45+.
  -p PIN_CODE, --pin_code PIN_CODE
                        The pin code. Use this option with search_type = pin.
```

## Example
### Search by district

```bash
python cowin-availability.py -s Karnataka -d BBMP -a 18
```

### Search by district

```bash
python cowin-availability.py -t pin -a 45 -p 560001
```