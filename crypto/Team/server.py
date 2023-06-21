import socket
import os
import sys
import subprocess
from time import sleep
import signal

X_n = 16794412573123108849144641243284499333226479542972962548827274686736025628196781086852560825888068968543149195495625730189467215629027883305315998750870034678424364685745794615939463009998236919824084983878641677569301715232557994731223048584991949088870881849116446565533537593758584907123464227921705600937699162038598176027910196801878799279225090196104965917660583884679475517285867166309896815494247975807149260839961608048596725948297378439376553566341600460653041999519202965757790798331086427449048906971405415061214174488752666148882956399678374446851116990439913776343205714293044197873548218778127289546862
m = 1 << 2048
a = 30984215072177141285134324829907083041300312208034108604363379093352270893551137730061842900332274087705839939062554877174339723740057833315412891534073519912633620675414301696847862389924871351315042198056361800723749766852600809020723247270497400180444693411105655923547669498752010434464920892449698495037711817501691259242445044483237313573117917944677394631323036487104295496609048241113026838294877864197099550569943408139263348146545784739184548243051784084851689822442358365800083110203354207638194295202764855724412174054395570535526091659668712705791581953601931566603793761721080899623597313834486943047281
c = 27388129613838411585203245069144566876332624210824672761659841770230731672195166759376327691170722192369445103301340936327860935462347779872199116689652586776745215487503909838340853033260394117846369808786772710924545519472324250224783441434013372583818700540308990398338958127163302916536250177617056028828633473092903928781892238883161965017175711523235867267161616004570569664243931808488522476290365991847044001504242459179320189898926794808009882030459058182570628648076484429308256449818743319301329982043485633112839312829594303088848997479137481381769377594450974034333199536112358615242695456498770442238685

'''
To run correctly:

In the file service.py change the destination port of request_trusted_center to port 1000X,
where "X" is your team's subnet number. 

For example: 
    Your address: 10.20.1.0; 
    Port: 10001; 

    Your address: 10.20.5.0; 
    Port: 10005; 
    
    And so on... 

Attention! 
The use of ports belonging to other teams will lead to a violation of the logic of the service, 
as a result of which the health check system will inform you 
about the incorrect operation of the service, which will affect the points you earn.
'''

def request_trusted_center():
    HOST = "10.20.100.10"
    PORT = 10001 #change me to your port number
    cmd = f'nc -w 2 {HOST} {PORT}'
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid).stdout.read()
    return data

def randint(N, V):
    global X_n
    r = 0
    while V - N >= r:
        X_n = (a * X_n + c) % m
        r = (r << 2048) + X_n
    return N + r % (V - N + 1)
    
def isPrime(p):
    if p <= 1:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    s, t = 0, p - 1
    while t % 2 == 0:
        s, t = s + 1, t >> 1
    for _ in range(256):
        a = randint(2, p - 2)
        x = pow(a, t, p)
        if x == 1 or x == p - 1:
            continue
        flag = False
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == 1:
                return False
            elif x == p - 1:
                flag = True
                break
        if flag:
            continue
        return False
    return True

def key_verification(y, g, p):
    if not isPrime(p):
        return 'Your number is composite'
    if not(2 <= g <= p - 2):
        return 'g does not lie in the range from [2 to p-2]'
    if not(1 <= y <= p - 1):
        return 'g does not lie in the range from [1 to p-1]'
    return 'the key has been verified'

def encrypt(m, y, g, p):
    k = int(request_trusted_center())
    a, b = pow(g, k, p), (pow(y, k, p) * m) % p
    return a, b

def decrypt(a, b, x, p):
    m = (b * pow(a, -x, p)) % p
    return m

def main():
    while True:
        print("\nList of actions:")
        print("0) Exit")
        print("1) Encrypt the message")
        print("2) Decrypt the message")
        print("3) Request a message log")
        action = input("\nSelect an action: ")
        
        if action == '0':
            break
        
        elif action == '1':
            print('\np is a large prime number\ng is the primitive root of the number p\nx is the private key\ny = pow(g, x, p)\n')
            try:
                p = int(input("Enter the p: "))
                g = int(input("Enter the g: "))
                y = int(input("Enter the y: "))
            except:
                print('Incorrect input, numbers are not integers')
                continue
            text = key_verification(y, g, p)
            print(text)
            if text != 'the key has been verified':
                continue
            message = input('Enter a message: ').encode()
            m = int.from_bytes(message, byteorder = 'big')
            a, b = encrypt(m, y, g, p)
            print(f'encrypted message: {a}, {b}')
            with open('message_protocol.txt', 'a') as file:
                file.write(f'p, g, y = {p}, {g}, {y}\nencrypted message: {a}, {b}\n')
            
        elif action == '2':
            print('\np is a large prime number\ng is the primitive root of the number p\nx is the private key\ny = pow(g, x, p)\n')
            try:
                p = int(input("Enter the p: "))
                g = int(input("Enter the g: "))
                y = int(input("Enter the y: "))
                x = int(input("Enter the x: "))
            except:
                print('Incorrect input, numbers are not integers')
                continue
            text = key_verification(y, g, p)
            print(text)
            if text != 'the key has been verified' or y != pow(g, x, p):
                continue
            print('\nCiphertext \na = pow(g, k, p)\nb = m*pow(y, k, p)\n')
            try:
                a = int(input("Enter the a: "))
                b = int(input("Enter the b: "))
            except:
                print('Incorrect input, numbers are not integers')
                continue
            print(f'message: {decrypt(a, b, x, p)}')
            
        elif action == '3':
            with open('message_protocol.txt', 'r') as file:
                print(file.read())

        elif action == '4':           
            cmd = 'ncat -l 7777 < message_protocol.txt'
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            sleep(20)
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

if __name__ == '__main__':
    main()



            
    
