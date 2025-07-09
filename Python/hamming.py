import random
import math 

def text_to_binary(text, joiner = ' '):
    return joiner.join(format(ord(char), '08b') for char in text)
def binary_to_text(binary, joiner=" "):
    if joiner:
        chunks = binary.split(joiner)
    else:
        chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chunks if len(b) == 8)

def noisy_channel(in_message, flip_rate=0.1):
    out_message = list(in_message)  
    for i in range(len(out_message)):
        if random.random() < flip_rate:
            if out_message[i] == "1":
                out_message[i] = "0"
            elif out_message[i] == "0":
                out_message[i] = "1"
    return ''.join(out_message) 

## NO ERROR CORRECTION
# transmit_message = "Hello my old heart" # my old heart, come to me"
# print(transmit_message)
# transmit_message_t2b = text_to_binary(transmit_message, "")
# print(transmit_message_t2b)
# received_message = noisy_channel(transmit_message_t2b)
# print(received_message)
# received_message_b2t = binary_to_text(received_message, "")
# print(received_message_b2t)

def bit3_sending(message, gap = 3):
    out_message = ""
    for i in range(len(message)):
        out_message += message[i]*gap
    return out_message

def bit3_receiving(message, n=3):
    out_bits = []
    for i in range(0, len(message), n):
        chunk = message[i:i+n]
        if len(chunk) < n:
            continue  # skip incomplete chunk
        ones = chunk.count('1')
        zeros = chunk.count('0')
        out_bits.append('1' if ones > zeros else '0')
    return ''.join(out_bits)


    
# ## Naive error correction, 3bit sending 
# transmit_message = "Hello my old heart"
# print(transmit_message)
# transmit_message_t2b = text_to_binary(transmit_message, "")
# print(transmit_message_t2b)
# transmit_message_error_correct = bit3_sending(transmit_message_t2b)
# print(transmit_message_error_correct)
# received_message = noisy_channel(transmit_message_error_correct, 0.1)
# print(received_message)
# received_message_error_correct = bit3_receiving(received_message)
# print(received_message_error_correct)
# received_message_b2t = binary_to_text(received_message_error_correct, "")
# print(received_message_b2t)


def hamming_code_transmit(message):
    def hamming_encode(chunk):
        c = [int(i) for i in list(chunk)]
        output =   [0   ,   0,   0,c[0],
                    0   ,c[1],c[2],c[3],
                    0   ,c[4],c[5],c[6],
                    c[7],c[8],c[9],c[10]]
        for j in range(4):
            output[2**j] = sum([output[i] for i in range(16) if (i >> j) & 1])%2
        output[0] = sum(output)%2
        return ''.join(str(i) for i in output)
    remainder = len(message) % 11
    if remainder != 0:
        message += '0' * (11 - remainder)
    chunks = [message [i:i+11] for i in range(0, len(message), 11)]
    output = ""
    for chunk in chunks:
        output += hamming_encode(chunk)
    return output
    
def hamming_code_recieve(message):
    def chunk_decode(c):
        out = ""
        for i in range(16):
            if i & (i - 1) != 0:
                out += str(c[i])
        return(out) 
    
    def hamming_decode(chunk):
        c = [int(i) for i in list(chunk)]
        if sum(c)%2 == 0:
            return chunk_decode(c)
        else:
            error_index = 0
            error_bit = []
            for j in range(4):
                error_bit.append(sum([c[i] for i in range(16) if (i >> j) & 1])%2)
            for i,p in enumerate(error_bit):
                error_index += 2**i * p
            # # print(error_index)
            c[error_index] ^= 1
            return chunk_decode(c)

    chunks = [message [i:i+16] for i in range(0, len(message), 16)]
    output = ""
    for chunk in chunks:
        output += hamming_decode(chunk)
    n = len(output)%8
    output = output[:len(output) - n]
    return output

# total_bit = "01001000"
# transmit_bit = hamming_code_transmit(total_bit)
# print(transmit_bit)

# error_bits = []
# for i in range(16):
#     # Make a mutable copy
#     bit_list = list(transmit_bit)
#     # Flip the bit
#     bit_list[i] = '0' if bit_list[i] == '1' else '1'
#     # Join and append
#     flipped = ''.join(bit_list)
#     error_bits.append(flipped)
# print(error_bits)

# decoded = []
# for error in error_bits:
#     decoded_list = hamming_code_recieve(error)
#     decoded.append(decoded_list)
# print(decoded)

def binary_to_ascii_recovery(bitstream):
    def closest_ascii_bits(binary_str):
        min_dist = float('inf')
        best_bits = '00000000'
        for i in range(32, 127):  # Printable ASCII range
            ascii_bits = format(i, '08b')
            dist = sum(a != b for a, b in zip(binary_str, ascii_bits))
            if dist < min_dist:
                min_dist = dist
                best_bits = ascii_bits
        return best_bits

    # Cut off trailing bits that aren't a full byte
    if len(bitstream) % 8 != 0:
        bitstream = bitstream[:-(len(bitstream) % 8)]

    corrected_binary = []
    for i in range(0, len(bitstream), 8):
        chunk = bitstream[i:i+8]
        corrected_binary.append(closest_ascii_bits(chunk))

    return ''.join(corrected_binary)


# # Hamming Code
# transmit_message = "I believe I have done pretty well with this paper. My main job was RnD and Data Analysis. I also compiled all the paper and passed it on time along with the others. I also participated in the experiment. Darwin made the methodology and conclusion on time, and also participated on the experiment. No complaints.. Lue made the introduction and abstract on time, and also participated in the experiment"
# # transmit_message = "This shit is pretty intense, no?"
# print(transmit_message)
# transmit_message_t2b = text_to_binary(transmit_message, "")
# print(transmit_message_t2b)
# transmit_message_error_correct = hamming_code_transmit(transmit_message_t2b)
# print(transmit_message_error_correct)
# received_message = noisy_channel(transmit_message_error_correct, 0.01)
# print(received_message)

# received_message_error_correct =  hamming_code_recieve(received_message)
# print(received_message_error_correct)
# print("--FIRST RECOVERY--")
# received_message_b2t = binary_to_text(received_message_error_correct, "")
# print(received_message_b2t)
# print("--SECOND RECOVERY--")
# recieved_message_ascii_closest = binary_to_ascii_recovery(received_message_error_correct)
# received_message_b2t = binary_to_text(recieved_message_ascii_closest, "")
# print(received_message_b2t)

## Triple Hamming + ASCII

transmit_message = "I believe I have done pretty well with this paper. My main job was RnD and Data Analysis. I also compiled all the paper and passed it on time along with the others. I also participated in the experiment. Darwin made the methodology and conclusion on time, and also participated on the experiment. No complaints.. Lue made the introduction and abstract on time, and also participated in the experiment"
# transmit_message = "This shit is pretty intense, no?"
print(transmit_message)
transmit_message_t2b = text_to_binary(transmit_message, "")
print(transmit_message_t2b)
transmit_message_3bredundancy = bit3_sending(transmit_message_t2b , 11)
print(transmit_message_3bredundancy)
transmit_message_error_correct = hamming_code_transmit(transmit_message_3bredundancy)
print(transmit_message_error_correct)

print("--NOISY CHANNEL--")
received_message = noisy_channel(transmit_message_error_correct, 0.125)
print(received_message)
print("--NOISY CHANNEL--") 

received_message_error_correct =  hamming_code_recieve(received_message)
print(received_message_error_correct)
received_message_3bit_correct = bit3_receiving(received_message_error_correct, 11)
print(received_message_3bit_correct )
print("--FIRST RECOVERY--")
received_message_b2t = binary_to_text(received_message_3bit_correct, "")
print(received_message_b2t)
print("--SECOND RECOVERY--")
recieved_message_ascii_closest = binary_to_ascii_recovery(received_message_3bit_correct)
received_message_b2t = binary_to_text(recieved_message_ascii_closest, "")
print(received_message_b2t)
