password = input("Enter new password: ")

results = {}

if len(password) >= 8:
    results["length"] = True
else:
    results["length"] = False

has_digit = False
for char in password:
    if char.isdigit():
        has_digit = True
        break

results["has_digit"] = has_digit

has_uppercase = False
for char in password:
    if char.isupper():
        has_uppercase = True
        break

results["has_uppercase"] = has_uppercase

if all(results.values()):
    print("Strong password")
else:
    print("Weak password")
