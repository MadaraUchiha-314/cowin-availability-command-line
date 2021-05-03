# cowin-availability-command-line
A command line utility to check the availability of vaccine slots

## Usage

```
python cowin-availability.py --help
usage: cowin-availability.py [-h] [-t {pin,district}] [-s STATE] [-d DISTRICT] [-a AGE_LIMIT] [-p PIN_CODE]

optional arguments:
  -h, --help            show this help message and exit
  -t {pin,district}, --search_type {pin,district}
                        The type of search to perform
  -s STATE, --state STATE
                        The name of the state
  -d DISTRICT, --district DISTRICT
                        The name of the district
  -a AGE_LIMIT, --age_limit AGE_LIMIT
                        The age limit
  -p PIN_CODE, --pin_code PIN_CODE
                        The pin code
```