import pdfplumber
import re

def gerarLinha(di_path):
    
    linha = {}

    coordinates = {
        'Processo': (102.2, 91.1, 151.2, 102.2),
        'DI': (85.4, 12.7, 151.0, 26.9),
        
        'II': (388, 435.4, 470.7, 450.7),
        'IPI': (388, 448.3, 470, 465.4),
        'PIS': (388, 461, 470, 480),
        'COFINS': (388, 475, 470, 495),
        'Antidumping': (388, 490, 470, 505),
    }
    
    patterns = {
        'VMLE': r"VMLE[^\d]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*)",
        'Frete': r"Frete[^\d]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*)",
        'Seguro': r"Seguro[^\d]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*)",
        'CIF': r"VMLE\+FRETE\+SEGURO[^\d]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*)",
        'Acréscimos': r"Acréscimos[^\d]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*)",
        
        'Capatazia': r"Capatazia[^\d]*(\d.*)",
        'Anuência LI': r"Taxa anuencia [^\d]*(\d.*)",
        'AFRMM': r"AFRMM[^\d]*(\d.*)",
        'Siscomex': r"TX siscomex[^\d]*(\d.*)",
    }
    
    with pdfplumber.open(di_path) as di:
        info = di.pages[1].extract_text()

        for field, bbox in coordinates.items():
            if coordinates[field] != None:
                
                pageNum = 1 if field == 'Processo' else 0 # Com excessão do processo, todos os campos estão na primeira página

                bboxInfo = di.pages[pageNum].within_bbox(bbox).extract_text()
                linha[field] = bboxInfo
                
        for field, pattern in patterns.items():
            
            match = re.search(pattern, info, re.IGNORECASE)

            if field == 'Capatazia' or field == 'Anuência LI' or field == 'AFRMM' or field == 'Siscomex':
                if match != None:
                    linha[field] = match.group(1)
                else:
                    linha[field] = 'Não encontrado'
            else:
                linha[field] = match.group(2)
    
    return linha
