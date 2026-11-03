# -*- coding: utf-8 -*-
import sys, time
from pathlib import Path
sys.path.insert(0, 'docs/scripts')
import convertir_pdf as cp
cp.DOCX_BUILD = Path(r'C:\temp\tfi_tesis_build\tesis_v6.docx')
cp.PDF_SALIDA = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf')
cp.MD_ORIGEN  = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.md')
import win32com.client
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
word.AutomationSecurity = 3
doc = None
try:
    print('abriendo')
    doc = word.Documents.Open(str(cp.DOCX_BUILD), ReadOnly=False, AddToRecentFiles=False)
    print('abierto')
    for name,fn in [('pagina',cp.preparar_pagina),('saltos',cp.arreglar_saltos),('cuerpo',cp.estilo_cuerpo),('titulos',cp.estilo_titulos),('portada',cp.estilo_portada),('tablas',cp.estilo_tablas),('espaciado',cp.espaciado_bloques),('figuras',cp.estilo_figuras),('indices',cp.estilo_indices),('numeracion',cp.numerar_paginas)]:
        print(name)
        fn(doc)
        time.sleep(1)
    print('numerando')
    cp.numerar_indices(doc)
    print('exportando')
    cp.exportar_pdf(doc, cp.PDF_SALIDA)
    print('DONE')
except Exception as e:
    print(e)
finally:
    if doc is not None:
        try: doc.Close(False)
        except: pass
    try: word.Quit()
    except: pass
