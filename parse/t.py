from hashlib import sha256


given = '000c674f83c1b49461e23de8dd7ae655fe1fbe91ae04590c513026f01b39d515f292c8c5c2fe9fd30ef1c632e6936edabe42f087e3cb50ceef0324b729383d82'

for i in range(10000):
    i_hashed = sha256(str(i).encode('utf-8')).hexdigest()
    print('i_hashed', i_hashed)
    s = ''.join([given, i_hashed])
    s_hashed = sha256(s.encode('utf-8')).hexdigest()
    if s_hashed.startswith('00'):
        print('FIN: i_hashed', i_hashed)
        print('THE NUM: ', i)
        print(sha256(s.encode('utf-8')).hexdigest())
        raise SystemExit(0)
    
