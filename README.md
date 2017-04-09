<p align="center">
    <img src="digiprice.png">
    CLI price search for electronic circuit components
</p>


# Purpose
Digiprice provides instant price quotes from Digi-Key, the world's largest catalog of electronic components.  

When designing mass-produced electronics, it pays to be price conscious. 
Every penny you shave off materials costs could equate to thousands of dollars saved annually.

Digiprice is fast and effortless. The intention is for engineers to leverage its convenience to more proactively compare prices and design with cost mindfulness. 

# Under the Hood
This tool relies on the exemplary Octopart API. 
If you've automated the use of this tool and are performing many searches, please register your own API key with Octopart. Set this in Digiprice with the --apikey flag.  

# Install 

## Linux or Mac
1. Clone this repository (or download it)
    ```shell
    $ git clone https://github.com/raykamp/digiprice
    ```
1. Install in /usr/local/bin
    ```shell
    $ sudo cp ./digiprice/digiprice.py /usr/local/bin/digiprice
    ```
1. Make digiprice an executable
    ```shell
    $ sudo chmod +x /usr/local/bin/digiprice
    ```

# Use

## Fast and Loose
```shell
$ digiprice NE555
NE555PSR 	 $0.07750 	 @ 	 100k   
```

## Strict
```shell
$ digiprice NE555PWR --strict
NE555PWR 	 $0.07750 	 @ 	 100k  
```

## Power User
```shell
$ digiprice NE555DR NSR0530HT1G CC2640R2FRGZT --strict
NE555DR 	 $0.08680 	 @ 	 12k  
NSR0530HT1G 	 $0.01536 	 @ 	 150k  
CC2640R2FRGZT 	 $4.18660 	 @ 	 100  
```

## Help Me
```shell
$ digiprice --help
```