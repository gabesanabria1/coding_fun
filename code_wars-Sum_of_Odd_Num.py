#link: https://www.codewars.com/kata/55fd2d567d94ac3bc9000064/train/python
#Daniel solution with debug printout

def row_sum_odd_numbers(n):
    count = 0
    sum = 0
    b = 0
    a = 0
    for i in range(n,0,-1):
        a = a + i
        print(f"a is {a}")
    print(f"the total numbers to end of {n} row are : {a}")
    for i in range ( a-1, (a-n-1), -1):
        b = (2*(i)+1)
        print(f"odd number: {b}")
        sum = sum + b
    print(f"sum: {sum}")
