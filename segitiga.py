def gambarSegitiga(tinggi):
    for i in range(1, tinggi + 1):
        print('\033[91m' + '*' * i)

tinggiSegitiga = 5
gambarSegitiga(tinggiSegitiga)
print('\033[0m')  
