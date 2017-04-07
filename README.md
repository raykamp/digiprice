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
$ digiprice 555
555 	 $0.14298 	 @ 	 2k 
```

## Strict
```shell
$ digiprice NE555DR --strict
NE555DR 	 $0.08680 	 @ 	 12k  
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