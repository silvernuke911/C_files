text_path = r'C:\Users\ADMIN\Documents\Code Stuff\Python\bezeir.txt'

text_endpath_hex = text_path.rsplit('.', 1)[0] + '_hex.txt'
text_endpath_dec = text_path.rsplit('.', 1)[0] + '_dec.txt'
text_endpath_bin = text_path.rsplit('.', 1)[0] + '_bin.txt'

# Read the file content
with open(text_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Convert content to ASCII decimal, hexadecimal, and binary
ascii_dec = [f"{ord(char):03d}" for char in content]  # 3-digit decimal
ascii_hex = [f"{ord(char):02X}" for char in content]  # Uppercase hex
ascii_bin = [f"{ord(char):08b}" for char in content]  # 8-bit binary

# Write ASCII decimal values
with open(text_endpath_dec, 'w') as file:
    file.write(' '.join(ascii_dec))

# Write ASCII hexadecimal values
with open(text_endpath_hex, 'w') as file:
    file.write(' '.join(ascii_hex))

# Write ASCII binary values
with open(text_endpath_bin, 'w') as file:
    file.write(' '.join(ascii_bin))

print("Conversion completed! Check 'sample_dec.txt' and 'sample_hex.txt'.")
