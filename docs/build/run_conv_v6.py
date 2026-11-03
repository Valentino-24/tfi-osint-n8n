import sys
sys.path.insert(0,'docs/scripts')
import convertir_pdf as cp
from pathlib import Path
import win32com.client
cp.DOCX_BUILD = Path(r'C:\temp\tfi_tesis_build\tesis_v6.docx')
cp.PDF_SALIDA = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf')
cp.MD_ORIGEN = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.md')
word = win32com.client.Dispatch('Word.Application')
word.Visible=False
word.DisplayAlerts=0
word.AutomationSecurity=3
doc = word.Documents.Open(str(cp.DOCX_BUILD),ReadOnly=False,AddToRecentFiles=False)
try:
    cp.preparar_pagina(doc)
    cp.arreglar_saltos(doc)
    cp.estilo_cuerpo(doc)
    cp.estilo_titulos(doc)
    cp.estilo_portada(doc)
    cp.estilo_tablas(doc)
    cp.espaciado_bloques(doc)
    cp.estilo_figuras(doc)
    cp.estilo_indices(doc)
    cp.numerar_paginas(doc)
    cp.numerar_indices(doc)
    cp.exportar_pdf(doc,cp.PDF_SALIDA)
    print('DONE')
finally:
    try: doc.Close(False)
    except: pass
    try: word.Quit()
    except: pass
