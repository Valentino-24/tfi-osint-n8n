# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, 'docs/scripts')
import convertir_pdf as cp

cp.DOCX_BUILD = Path(r'C:\temp\tfi_tesis_build\tesis_v6.docx')
cp.PDF_SALIDA = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf')
cp.MD_ORIGEN  = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.md')

import win32com.client
word = win32com.client.Dispatch('Word.Application')
word.Visible = True
word.DisplayAlerts = 0
try:
    word.AutomationSecurity = 3
except Exception:
    pass
doc = None
try:
    print('[word] abriendo...', flush=True)
    doc = word.Documents.Open(str(cp.DOCX_BUILD), ReadOnly=False, AddToRecentFiles=False)
    pasos = (('pagina', cp.preparar_pagina), ('saltos', cp.arreglar_saltos),
             ('cuerpo', cp.estilo_cuerpo), ('titulos', cp.estilo_titulos),
             ('portada', cp.estilo_portada), ('tablas', cp.estilo_tablas),
             ('espaciado', cp.espaciado_bloques), ('figuras', cp.estilo_figuras),
             ('indices', cp.estilo_indices), ('numeracion', cp.numerar_paginas))
    for nombre, paso in pasos:
        print(f'[word] {nombre}...', flush=True)
        paso(doc)
    print('[word] numerando indices...', flush=True)
    cp.numerar_indices(doc)
    print('[word] exportando PDF...', flush=True)
    cp.exportar_pdf(doc, cp.PDF_SALIDA)
    print('[word] DONE', flush=True)
finally:
    if doc is not None:
        try:
            doc.Close(SaveChanges=False)
        except Exception:
            pass
    try:
        word.Quit()
    except Exception:
        pass
