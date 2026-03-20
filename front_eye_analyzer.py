import cv2
import numpy as np
from PIL import Image

def analyze_front_eye(image_pil):
    img     = np.array(image_pil.convert('RGB'))
    results = {}
    hsv       = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_red1 = np.array([0,   50,  50])
    upper_red1 = np.array([10,  255, 255])
    lower_red2 = np.array([160, 50,  50])
    upper_red2 = np.array([180, 255, 255])
    mask1      = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2      = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask   = mask1 + mask2
    red_ratio  = red_mask.sum() / (255 * img.shape[0] * img.shape[1])
    results['Redness / Conjunctivitis'] = min(red_ratio * 8, 1.0)
    gray    = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w    = gray.shape
    top_half = gray[:h//2, :]
    edges    = cv2.Canny(top_half, 50, 150)
    edge_density = edges.sum() / (255 * top_half.size)
    results['Swelling / Puffiness'] = min(edge_density * 15, 1.0)
    lab         = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    b_channel   = lab[:, :, 2].astype(float)
    yellow_mean = b_channel.mean()
    jaundice_score = max(0, (yellow_mean - 120) / 60)
    results['Jaundice'] = min(jaundice_score, 1.0)
    gray_blur  = cv2.GaussianBlur(gray, (15,15), 0)
    circles    = cv2.HoughCircles(
        gray_blur, cv2.HOUGH_GRADIENT, 1, 30,
        param1=50, param2=30, minRadius=10, maxRadius=80)
    if circles is not None:
        cx, cy, r = map(int, circles[0][0])
        pupil_roi  = gray[max(0,cy-r):cy+r, max(0,cx-r):cx+r]
        if pupil_roi.size > 0:
            brightness = pupil_roi.mean()
            cataract_score = max(0, (brightness - 40) / 100)
            results['Cataract'] = min(cataract_score, 1.0)
        else:
            results['Cataract'] = 0.1
    else:
        results['Cataract'] = 0.1
    top_region    = gray[:h//3, w//4:3*w//4]
    bottom_region = gray[2*h//3:, w//4:3*w//4]
    top_bright    = top_region.mean()
    bottom_bright = bottom_region.mean()
    ptosis_score  = max(0, (bottom_bright - top_bright) / 100)
    results['Drooping Eyelid (Ptosis)'] = min(ptosis_score, 1.0)
    return results

def get_front_eye_recommendations(results):
    recommendations = []
    high_risk = []
    for condition, score in results.items():
        if score > 0.6:
            high_risk.append(condition)
        if score > 0.4:
            if condition == 'Redness / Conjunctivitis':
                recommendations.append("Possible conjunctivitis — avoid touching eyes, consult a doctor if persists beyond 2 days")
            elif condition == 'Swelling / Puffiness':
                recommendations.append("Eye swelling detected — apply cold compress, seek medical attention if painful")
            elif condition == 'Jaundice':
                recommendations.append("Yellowing of eyes detected — this may indicate liver issues, consult a doctor immediately")
            elif condition == 'Cataract':
                recommendations.append("Possible cataract — schedule a detailed eye examination with an ophthalmologist")
            elif condition == 'Drooping Eyelid (Ptosis)':
                recommendations.append("Eyelid drooping detected — consult a specialist to rule out neurological causes")
    needs_fundus = any(results.get(c, 0) > 0.5 for c in ['Cataract', 'Drooping Eyelid (Ptosis)'])
    return recommendations, high_risk, needs_fundus
