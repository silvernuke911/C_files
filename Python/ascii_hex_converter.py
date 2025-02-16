hex_path = r'C:\Users\ADMIN\Documents\Code Stuff\Python\donuter_hex.txt'

# Read the hex file
with open(hex_path, 'r', encoding='utf-8') as file:
    hex_content = file.read().split()

# Convert hex values to ASCII characters
ascii_text = ''.join(chr(int(hex_val, 16)) for hex_val in hex_content)

# Print the translated ASCII text
print("Decoded ASCII text:")
print(ascii_text)