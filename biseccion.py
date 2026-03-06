def f(x):
    return x**2 + 3*x - 6

def biseccion(a,b,err,max_i):
    # Casos base
    if f(a)*f(b)>0:
        return None
    x = (a+b)/2
    if abs(f(x)) < err or max_i<=0: 
        return x
    # Opciones
    if f(x) * f(a) < 0:
        x = biseccion(a,x,err,max_i-1)
    else:
        x = biseccion(x,b,err,max_i-1)
    return x

print('x ≈ ',biseccion(0,3,0.01,10))