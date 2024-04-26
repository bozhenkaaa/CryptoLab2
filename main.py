import hashlib
import timeit
import random
import math

class RSA:
    def __init__(self, bit_length):
        self.p = self.generate_prime_number(bit_length)
        self.q = self.generate_prime_number(bit_length)
        self.n = self.p * self.q
        self.phi = self.lcm(self.p - 1, self.q - 1)
        self.e = self.find_e()
        self.d = self.find_d()

    def lcm(self, a, b):
        return abs(a*b) // math.gcd(a, b)

    def miller_rabin_test(self, number, iteration=5):
        if number == 2 or number == 3:
            return True

        if number <= 1 or number % 2 == 0:
            return False

        r, s = 0, number - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(iteration):
            a = random.randrange(2, number - 1)
            x = pow(a, s, number)
            if x == 1 or x == number - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, number)
                if x == number - 1:
                    break
            else:
                return False
        return True

    def generate_prime_number(self, bit_length):
        while True:
            number = random.getrandbits(bit_length)
            if self.miller_rabin_test(number):
                return number

    def find_e(self):
        e = 2
        while self.gcd(e, self.phi) != 1:
            e += 1
        return e

    def find_d(self):
        d = 2
        while (d * self.e) % self.phi != 1:
            d += 1
        return d

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def encrypt(self, message):
        return [pow(ord(char), self.e, self.n) for char in message]

    def decrypt(self, encrypted_message):
        return ''.join(chr(pow(char, self.d, self.n)) for char in encrypted_message)

    def sign(self, message):
        message_hash = int(hashlib.sha1(message.encode()).hexdigest(), 16)
        message_hash = message_hash & ((1 << bit_length) - 1)  # take the last bit_length bits
        signature = pow(message_hash, self.d, self.n)
        return signature

    def verify(self, message, signature):
        message_hash = int(hashlib.sha1(message.encode()).hexdigest(), 16)
        message_hash = message_hash & ((1 << bit_length) - 1)  # take the last bit_length bits
        decrypted_hash = pow(signature, self.e, self.n)
        return message_hash == decrypted_hash

class Alice:
    def __init__(self, rsa):
        self.rsa = rsa

    def send_message(self, message):
        encrypted_message = self.rsa.encrypt(message)
        signature = self.rsa.sign(message)
        return encrypted_message, signature

class Bob:
    def __init__(self, rsa):
        self.rsa = rsa

    def receive_message(self, encrypted_message, signature):
        decrypted_message = self.rsa.decrypt(encrypted_message)
        if self.rsa.verify(decrypted_message, signature):
            print("The signature is valid.")
        else:
            print("The signature is not valid.")
        return decrypted_message

def hash_message(message):
    return hashlib.sha1(message.encode()).hexdigest()

start_time = timeit.default_timer()

bit_length = 16
rsa = RSA(bit_length)

alice = Alice(rsa)
bob = Bob(rsa)

message = "Hello, Bob!"
print("Original message: ", message)

encrypted_message, signature = alice.send_message(message)
print("Encrypted message: ", encrypted_message)
print("Signature: ", signature)

decrypted_message = bob.receive_message(encrypted_message, signature)
print("Decrypted message: ", decrypted_message)

hash_of_message = hash_message(message)
print("Hash of message: ", hash_of_message)

elapsed = timeit.default_timer() - start_time
print("Execution time: ", elapsed)