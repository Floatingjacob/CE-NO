import base64
import os
from PIL import Image
import zipfile
import io

binary_color_map = {
    '00': (0, 0, 0),
    '01': (255, 0, 0),
    '10': (0, 255, 0),
    '11': (0, 0, 255),
}

repetition_color_map = {
    3: (255, 255, 0),
    5: (0, 255, 255),
    7: (255, 0, 255),
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def encode(data):
    binary_data = ''.join(format(byte, '08b') for byte in data.encode('utf-8'))
    colored_data = []
    
    for i in range(0, len(binary_data), 2):
        chunk = binary_data[i:i+2]
        if len(chunk) < 2:
            chunk = chunk + '0'
        
        colored_data.append(binary_color_map[chunk])
    
    return colored_data

def save_file(file_path, zip_file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    encoded_data = base64.b64encode(file_data).decode('utf-8')
    colored_data = encode(encoded_data)
    
    grid_size = int(len(colored_data) ** 0.5) + 1
    img_size = grid_size * 5
    
    img = Image.new('RGB', (img_size, img_size), color='white')
    pixels = img.load()
    
    for i in range(len(colored_data)):
        x = (i % grid_size) * 5
        y = (i // grid_size) * 5
        color = colored_data[i]
        
        for dx in range(5):
            for dy in range(5):
                pixels[x + dx, y + dy] = color

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG", optimize=True)
    img_buffer.seek(0)
    
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.writestr("color_ce,no.png", img_buffer.read())

    img_buffer.close()
    print(f"ZIP file created: {zip_file_path}")

file_path = input("Enter the path to the file you want to encode: ")
zip_file_path = input("Enter the path to save the ZIP file with CE,NO: ")

save_file(file_path, zip_file_path)
