import pdfplumber
import re

def gerarLinha(di_path):
    
    linha = {}
    
    patterns = {
        #Coluna: (Página -1, Padrão)
        'Processo': r"REF\. CLIENTE[^\d]*? (.*\d[a-z])",
        'DI': r"Declaração[^\d\n]*(.*?-\d)",
        
        'II': r"I\.I\..*?,\d{2} (.*)",
        'IPI': r"I\.P\.I\..*?,\d{2} (.*\d)",
        'PIS': r"Pis/Pasep.*?,\d{2} (.*\d)",
        'COFINS': r"Cofins.*?,\d{2} (.*\d)",
        
        'VMLE': r"VMLE[^\d\n]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*\d)",
        'Frete': r"Frete[^\d\n]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*\d)",
        'Seguro': r"Seguro[^\d\n]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*\d)",
        'CIF': r"VMLE\+FRETE\+SEGURO[^\d\n]*(\d.*?,\d{2}) / (\d.*?,\d{2}) / (\d.*\d)",
        
        'Capatazia': r"Capatazia - [^\d\n]*(\d.*\d)",
        'AFRMM': r"AFRMM - [^\d\n]*(\d.*\d)",
        'Siscomex': r"TX siscomex - [^\d\n]*(\d.*\d)",
    }
    
    with pdfplumber.open(di_path) as di:
        
        for field, pattern in patterns.items():
            
            match field:
                case 'VMLE' | 'Frete' | 'Seguro' | 'CIF':
                    groupIndex = 2
                case _:
                    groupIndex = 1
                
            info = ''
            
            for page in di.pages:
                info += page.extract_text() + '\n\n\n\n'
            
            match = re.search(pattern, info, re.IGNORECASE)
            
            if field == 'Processo' and match == None:
                match = re.search(r"REF\. CLIENTE[^\d]*? (.*\d)", info, re.IGNORECASE)
                
            
            if match != None:
                linha[field] = match.group(groupIndex)
            else:
                linha[field] = 'Não encontrado'
        
    return linha