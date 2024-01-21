
def fibonnacci():
    fib_prev,fib = 0,1
    final = 0
    result = 0
    while result < 3000000:
        result = fib + fib_prev
        fib_prev = fib
        fib = result
        if result % 2 == 0:
            final = final + result
    return final

print(fibonnacci())