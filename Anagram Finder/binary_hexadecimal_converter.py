# FIT2085 Prac 1 Question 2

def print_menu() -> None:
    print('\nMenu:')
    print('1. Decimal to Binary')
    print('2. Decimal to Hexadecimal')
    print('3. Quit')

selected_quit = False

while not selected_quit:
    print_menu()
    command = int(input("\nEnter command: "))
    rem = 9999
    if command == 1:
        '''Converts decimal format to binary format

        Divides n by 2, takes the remainder, this repeats until n equals zero. Then prints the binary
        equivalent from last to first.
        '''
        n = int(input("\nEnter number to be converted into binary: "))
        binary = ""

        while n != 0:
            rem = n % 2
            n = n // 2
            binary = str(rem) + binary

        print("Binary equivalent: " + binary)
    elif command == 2:
        '''Converts decimal format to binary format

        Divides n by 16, takes the remainder, this repeats until n equals zero. Then prints the hexadecimal
        equivalent from last to first.
        '''
        n = int(input("\nEnter number to be converted into hexadecimal: "))
        hexadec = ""

        while n != 0:
            rem = n % 16
            n = n // 16
            
            if rem > 9:
                if rem == 10:
                    rem = "A"
                elif rem == 11:
                    rem = "B"
                elif rem == 12:
                    rem = "C"
                elif rem == 13:
                    rem = "D"
                elif rem == 14:
                    rem = "E"
                elif rem == 15:
                    rem = "F"
                elif rem == 16:
                    rem = "G"
            
            hexadec = str(rem) + hexadec
            
        print("Hexadecimal equivalent: " + hexadec)
    elif command == 3:
        selected_quit = True
