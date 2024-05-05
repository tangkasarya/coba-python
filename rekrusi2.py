def fibonacci(n):
    if n < 1:
        return [n]
    
    listSebelumN = fibonacci(n - 1)
    angkal = listSebelumN[-2] if len(listSebelumN) > 2 else 0
    angka = listSebelumN[-1] if len(listSebelumN) > 1 else 1
    
    return listSebelumN + [angkal + angka]

panjang = int(input('Masukkan panjang deret: '))
print(fibonacci(panjang))
