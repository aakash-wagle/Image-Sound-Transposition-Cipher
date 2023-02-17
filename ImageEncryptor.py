import random
from PIL import Image

def encrypt_image(image_file):
    # Open image file
    image = Image.open(image_file)
    width, height = image.size

    # Convert image to binary data
    binary_data = ""
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += '{:08b}{:08b}{:08b}'.format(r, g, b)

    # Generate random key length
    key_length = random.randint(1, width * height)

    # Apply transposition cipher on binary data
    encrypted_data = ""
    for i in range(0, len(binary_data), key_length):
        block = binary_data[i:i+key_length]
        encrypted_data += block[::-1]

    # Save encrypted image
    encrypted_image = Image.new('RGB', (width, height))
    pixels = encrypted_image.load()
    for y in range(height):
        for x in range(width):
            start = (y * width + x) * 24
            end = start + 24
            rgb = [int(encrypted_data[start+i:start+i+8], 2) for i in range(0, 24, 8)]
            r, g, b = rgb
            pixels[x, y] = (r, g, b)

    encrypted_image.save('encrypted.png')
    print("Image encrypted and saved as encrypted.png")
    return encrypted_data, key_length


def decrypt_image(image_file, key_length):
    # Open image file
    image = Image.open(image_file)
    width, height = image.size

    # Convert image to binary data
    binary_data = ""
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += '{:08b}{:08b}{:08b}'.format(r, g, b)

    # Apply transposition cipher on binary data
    decrypted_data = ""
    for i in range(0, len(binary_data), key_length):
        block = binary_data[i:i+key_length]
        decrypted_data += block[::-1]

    # Convert binary data to image
    decrypted_image = Image.new('RGB', (width, height))
    pixels = decrypted_image.load()
    for y in range(height):
        for x in range(width):
            start = (y * width + x) * 24
            end = start + 24
            rgb = [int(decrypted_data[start+i:start+i+8], 2) for i in range(0, 24, 8)]
            r, g, b = rgb
            pixels[x, y] = (r, g, b)

    decrypted_image.save('decrypted.png')
    print("Image decrypted and saved as decrypted.png")

if __name__=='__main__':
    e,k = encrypt_image('87760.jpg')
    decrypt_image('encrypted.png', k)