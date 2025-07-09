import re

run = True

while run :
    print("----------------------------------------")
    print("Gimme the fucking RGB Values:") #
    result = input("> ").strip()
    if result == "QUIT":
        run = False
    result = re.split(r'[ .\s]+', result)

    if len(result) != 3:
        print("Error: Must provide exactly 3 values.")
        continue

    try:
        rgb = [int(x) for x in result]
        if any((n < 0 or n > 255) for n in rgb):
            print("Error: Values must be between 0 and 255.")
            continue
    except ValueError:
        print("Error: All inputs must be integers.")
        continue

    hex_rgb = [f"{n:02X}" for n in rgb]
    print("----------------------------------------")
    print("#" + ''.join(hex_rgb))
    break
