import random


def generate_password(pwlength):
    alphabet = "abcdefghijklmnopqrstuvwxyz!@#$%^&*"
    passwords = []
    for i in pwlength:
        password = ""
        for j in range(i):
            next_letter_index = random.randrange(len(alphabet))
            password = password + alphabet[next_letter_index]
        password = replace_with_number(password)
        password = replace_with_uppercase_letter(password)
        passwords.append(password)
    return passwords


def replace_with_number(pword):
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(pword) // 2)
        pword = pword[0:replace_index] + str(random.randrange(10)) + pword[replace_index + 1:]
        return pword


def replace_with_uppercase_letter(pword):
    for i in range(random.randrange(1, 3)):
        replace_index = random.randrange(len(pword) // 2, len(pword))
        pword = pword[0:replace_index] + pword[replace_index].upper() + pword[replace_index + 1:]
        return pword


def main():
    num_passwords = 20
    # int(input("How many passwords do you want to generate? "))
    print("Generating " + str(num_passwords) + " passwords")
    password_lengths = []
    print("Minimum length of password should be 3")
    for i in range(num_passwords):
        length = random.randint(10, 15)
        password_lengths.append(length)
    password = generate_password(password_lengths)
    for i in range(num_passwords):
        print("Password #" + str(i + 1) + " = " + password[i])


main()
