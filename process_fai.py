import os
import re
import pandas as pd
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

# 初始化輕量 CPU 辨識模型
ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False)

def run_fai_extraction(pdf_path, output_csv_path):
    pages = convert_from_path(pdf_path, dpi=300)
    temp_img = "temp_process.png"
    pages[0].save(temp_img, "PNG")
    
    result = ocr.ocr(temp_img, cls=False)
    fai_rows = []
    
    if result and result[0]:
        for line in result[0]:
            text = line[1][0].strip()
            confidence = line[1][1]
            box = line[0]
            
            if any(char.isdigit() for char in text):
                center_x = (box[0][0] + box[2][0]) / 2
                center_y = (box[0][1] + box[2][1]) / 2
                
                nominal_value = text
                upper_limit = ""
                lower_limit = ""
                
                # 基礎公差切分邏輯
                if "+/-" in text:
                    parts = text.split("+/-")
                    nominal_value = parts[0].strip()
                    try:
                        tol = float(parts[1].strip())
                        nom = float(re.sub(r'[^\d.]', '', nominal_value))
                        upper_limit = f"{nom + tol:.3f}"
                        lower_limit = f"{nom - tol:.3f}"
                    except:
                        pass

                fai_rows.append({
                    "原始辨識內容": text,
                    "名義數值(Nominal)": nominal_value,
                    "公差上限(Upper)": upper_limit,
                    "公差下限(Lower)": lower_limit,
                    "X座標": center_x,
                    "Y座標": center_y,
                    "AI信心度": f"{confidence:.2f}"
                })
                
    if os.path.exists(temp_img):
        os.remove(temp_img)
        
    if not fai_rows:
        return False
        
    df = pd.DataFrame(fai_rows)
    # 按幾何座標排序
    df = df.sort_values(by=["Y座標", "X座標"]).reset_index(drop=True)
    df.to_csv(output_csv_path, index=True, index_label="FAI預估序號", encoding="utf-8-sig")
    return True