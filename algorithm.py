def create_password(password_range:int | str ="" ,_lowercase=True,_uppercase=False,_digits=False,_punctuation=False):
    from string import ascii_lowercase,ascii_uppercase,digits,punctuation
    from itertools import product

    symbols = ''
    start = end = 0
    flag = True

    cnt = 1

    if _lowercase:
        symbols += ascii_lowercase
    if _uppercase:
        symbols += ascii_uppercase
    if _digits:
        symbols += digits
    if _punctuation:
        symbols += punctuation
    if isinstance(password_range,str):
        try:
            if '-' in password_range:
                start,end = map(int,password_range.split('-'))
            else:
                start = end = int(password_range)
        except Exception as err:
            flag = False
            print(err)
            return "password error",flag,-1
    else:
        start = end = round(password_range)

    for n in range(start,end+1):
        for i in product(symbols,repeat=n):
            yield ''.join(i),round(cnt/len(symbols)**n,5)
            cnt += 1

