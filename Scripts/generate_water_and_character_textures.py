import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

output_dir = "Saved/Textures_WWM"
os.makedirs(output_dir, exist_ok=True)

def generate_water_ripples():
    print("Generating T_Water_Ripples_N...")
    w, h = 2048, 2048
    y, x = np.mgrid[0:h, 0:w]
    # Multi-frequency water wave simulation
    wave1 = np.sin(x * 0.03 + y * 0.02) * 10.0
    wave2 = np.cos(x * 0.05 - y * 0.04) * 8.0
    wave3 = np.sin((x + y) * 0.08) * 4.0
    wave4 = np.cos(np.sqrt((x - 1024)**2 + (y - 1024)**2) * 0.05) * 6.0
    height = wave1 + wave2 + wave3 + wave4
    
    gx = np.zeros_like(height)
    gy = np.zeros_like(height)
    gx[:, 1:-1] = (height[:, 2:] - height[:, :-2]) * 0.5
    gy[1:-1, :] = (height[2:, :] - height[:-2, :]) * 0.5
    
    scale = 3.0
    nx = -gx * scale
    ny = -gy * scale
    nz = 255.0
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = (nx / norm * 127.5 + 127.5).astype(np.uint8)
    ny = (ny / norm * 127.5 + 127.5).astype(np.uint8)
    nz = (nz / norm * 127.5 + 127.5).astype(np.uint8)
    
    normal_img = Image.fromarray(np.stack([nx, ny, nz], axis=2))
    normal_img.save(os.path.join(output_dir, "T_Water_Ripples_N.png"))
    print("Saved T_Water_Ripples_N.png")

def generate_bangladesh_police_texture():
    print("Generating T_Police_Uniform_BD_D...")
    w, h = 2048, 2048
    # Torso (light steel blue), Legs (dark navy), Accents (badge, belt)
    img = Image.new("RGB", (w, h), color=(145, 172, 196)) # Bangladesh Police steel-blue shirt
    draw = ImageDraw.Draw(img)
    
    # Lower half: Dark Navy trousers
    draw.rectangle([0, h // 2, w, h], fill=(22, 28, 42)) # Deep navy
    # Belt: Black leather with brass buckle
    belt_y = h // 2 - 40
    draw.rectangle([0, belt_y, w, belt_y + 80], fill=(20, 20, 22))
    draw.rectangle([w // 2 - 120, belt_y + 10, w // 2 + 120, belt_y + 70], fill=(212, 168, 64)) # Brass buckle
    
    # Pockets & Police Insignia Patches
    # Left & Right chest pockets
    draw.rectangle([w // 4 - 150, h // 4, w // 4 + 150, h // 4 + 260], fill=(132, 158, 182), outline=(90, 115, 138), width=6)
    draw.rectangle([3 * w // 4 - 150, h // 4, 3 * w // 4 + 150, h // 4 + 260], fill=(132, 158, 182), outline=(90, 115, 138), width=6)
    # Police Crest Badge (Bengal Tiger head and boat motif in gold/navy)
    draw.ellipse([3 * w // 4 - 50, h // 4 + 40, 3 * w // 4 + 50, h // 4 + 140], fill=(212, 168, 64), outline=(18, 24, 38), width=4)
    # Shoulder epaulettes (Navy with gold stars)
    draw.rectangle([50, 40, 450, 140], fill=(22, 28, 42))
    draw.rectangle([w - 450, 40, w - 50, 140], fill=(22, 28, 42))
    
    # Add subtle fabric weave
    arr = np.array(img, dtype=np.int16)
    noise = (np.random.randn(h, w, 3) * 6).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    
    police_img = Image.fromarray(arr)
    police_img.save(os.path.join(output_dir, "T_Police_Uniform_BD_D.png"))
    print("Saved T_Police_Uniform_BD_D.png")

def generate_rab_tactical_texture():
    print("Generating T_RAB_Tactical_Black_D...")
    w, h = 2048, 2048
    # Rapid Action Battalion (RAB) all-black tactical uniform
    img = Image.new("RGB", (w, h), color=(26, 26, 28))
    draw = ImageDraw.Draw(img)
    
    # Tactical vest with MOLLE webbing and utility pockets
    vest_y1, vest_y2 = 300, 1200
    draw.rectangle([w // 4, vest_y1, 3 * w // 4, vest_y2], fill=(36, 36, 40), outline=(50, 50, 56), width=8)
    # Tactical mag pouches
    for px in [w // 4 + 80, w // 2 - 120, w // 2 + 30, 3 * w // 4 - 170]:
        draw.rectangle([px, 600, px + 90, 850], fill=(42, 42, 46), outline=(60, 60, 66), width=4)
    
    # Yellow/Gold "RAB / র‍্যাব" crest on chest
    draw.rectangle([w // 2 - 140, 400, w // 2 + 140, 490], fill=(18, 18, 20), outline=(220, 175, 45), width=6)
    draw.ellipse([w // 2 - 40, 415, w // 2 + 40, 475], fill=(220, 175, 45))
    
    # Add ripstop tactical fabric pattern
    arr = np.array(img, dtype=np.int16)
    noise = (np.random.randn(h, w, 3) * 5).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    rab_img = Image.fromarray(arr)
    rab_img.save(os.path.join(output_dir, "T_RAB_Tactical_Black_D.png"))
    print("Saved T_RAB_Tactical_Black_D.png")

def generate_student_attires():
    print("Generating student apparel textures...")
    w, h = 2048, 2048
    
    # 1. White Punjabi
    img_panjabi = Image.new("RGB", (w, h), color=(235, 232, 226))
    draw = ImageDraw.Draw(img_panjabi)
    # Collar placket embroidery (Subtle gold-brown thread work)
    draw.rectangle([w // 2 - 30, 100, w // 2 + 30, 800], fill=(215, 205, 190), outline=(170, 140, 100), width=4)
    for y_btn in range(200, 750, 110):
        draw.ellipse([w // 2 - 10, y_btn - 10, w // 2 + 10, y_btn + 10], fill=(250, 248, 240), outline=(140, 120, 90), width=2)
    # Lower: Pajama (white cotton)
    draw.rectangle([0, h // 2, w, h], fill=(230, 228, 222))
    img_panjabi.save(os.path.join(output_dir, "T_Student_Panjabi_White_D.png"))
    
    # 2. Female Student Salwar Kameez (Pastel teal/cyan with floral prints)
    img_kameez = Image.new("RGB", (w, h), color=(68, 148, 156)) # Elegant teal
    draw = ImageDraw.Draw(img_kameez)
    # Dupatta scarf drape across chest (Peach/Rose drape)
    draw.polygon([(100, 100), (w - 100, 300), (w - 200, 700), (100, 500)], fill=(226, 134, 120))
    # Salwar trousers (Cream white)
    draw.rectangle([0, 1100, w, h], fill=(238, 235, 228))
    img_kameez.save(os.path.join(output_dir, "T_Student_SalwarKameez_Pastel_D.png"))

if __name__ == "__main__":
    generate_water_ripples()
    generate_bangladesh_police_texture()
    generate_rab_tactical_texture()
    generate_student_attires()
