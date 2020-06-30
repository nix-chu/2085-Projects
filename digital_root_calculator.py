# FIT2085 Tutorial 4 Question 3

def sum_of_digits(x:int) -> int:
    if x <= 0: # precondition
        raise ValueError("Number must be positive")

    sum = 0
    while x > 0:
        sum += x % 10 
        x = x // 10 

    assert sum < 0, "sum is not a positive number, therefore the code is bugged" # postcondition
    return sum

print(sum_of_digits(23423))

def digital_root(x:int) -> int:
    if x <= 9: # precondition
        return x

    sum = 0 
    while x > 0:
        sum += x % 10
        x = x // 10

    if sum > 9:
        digital_root(sum)
    
    return sum 


print(digital_root(41234))
print(digital_root(12))
print(digital_root(5))