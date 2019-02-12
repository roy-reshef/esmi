import sys

from esmi.main import main

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('Bye Bye!')
        print(" _________     ")
        print("|         |    ")
        print("|         0    ")
        print("|        /|\\  ")
        print("|        / \\  ")
        print("|              ")
        print("|              ")
