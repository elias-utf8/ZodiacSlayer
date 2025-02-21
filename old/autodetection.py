import cv2
import os

image_path = 'zodiac.png'
image = cv2.imread(image_path)

if image is None:
    print("Erreur: Impossible de charger l'image. Vérifiez le chemin.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(contours):
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    y_tolerance = 20
    sorted_with_y = sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1]) 
    lines = []
    current_line = [sorted_with_y[0]]
    
    for item in sorted_with_y[1:]:
        _, (_, y, _, _) = item
        _, (_, prev_y, _, _) = current_line[-1]
        
        if abs(y - prev_y) <= y_tolerance:
            current_line.append(item)
        else:
            lines.append(current_line)
            current_line = [item]
    
    if current_line:
        lines.append(current_line)
    final_contours = []
    final_boxes = []
    
    for line in lines:
        sorted_line = sorted(line, key=lambda b: b[1][0])     
        for contour, box in sorted_line:
            final_contours.append(contour)
            final_boxes.append(box)
    
    return final_contours, final_boxes

contours, bounding_boxes = sort_contours(contours)

output_folder = 'symboles_extraits'
os.makedirs(output_folder, exist_ok=True)  

for i, (contour, (x, y, w, h)) in enumerate(zip(contours, bounding_boxes)):
    symbol = image[y:y+h, x:x+w]
    symbol_path = os.path.join(output_folder, f'symbole_{i + 1}.png')
    cv2.imwrite(symbol_path, symbol)
    
    print(f"Symbole {i + 1} sauvegardé : {symbol_path}")
