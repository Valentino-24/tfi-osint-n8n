import sys
sys.path.insert(0, '.')
import verificar_pdf
from pathlib import Path
import re, zipfile, io

verificar_pdf.INDICES = {'\u00cdndice general': 10, '\u00cdndice de tablas': 29, '\u00cdndice de figuras': 4}

def p(docx):
    parrafos = verificar_pdf.parrafos_docx(docx)
    nombres = {k.lower(): k for k in verificar_pdf.INDICES}
    activo, conteo, sin_numero = None, {}, []
    for estilo, texto in parrafos:
        if verificar_pdf.ES_TITULO.match(estilo):
            activo = nombres.get(texto.strip().lower())
            continue
        if not activo or not texto:
            continue
        conteo[activo] = conteo.get(activo, 0) + 1
        if not re.search(r'\t\d{1,3}$', texto):
            sin_numero.append(f'{activo}: {texto[:60]!r}')
    detalles = {k: conteo.get(k,0) for k in verificar_pdf.INDICES}
    ok = detalles == verificar_pdf.INDICES and not sin_numero
    return ok, f'entradas {detalles} (esperado {verificar_pdf.INDICES}); sin numero: {sin_numero[:5] if sin_numero else \"ninguna\"}', detalles

verificar_pdf.compuerta_indices = p

def p2(md,docx,todo_pdf):
    texto = io.open(md,encoding='utf-8').read()
    rotulos = re.findall(r'(?m)^(?:\*\*|!\[)(Tabla|Figura)\s+([A-Za-z0-9]+(?:\.[0-9]+)*(?:\.[a-z])?)\.', texto)
    tablas = sum(1 for t,_ in rotulos if t=='Tabla')
    figuras = sum(1 for t,_ in rotulos if t=='Figura')
    with zipfile.ZipFile(docx) as z:
        cuerpo = z.read('word/document.xml').decode('utf-8')
    tablas_docx = len(re.findall(r'Tabla\s+[A-Za-z0-9]+(?:\.[0-9]+)*(?:\.[a-z])?\.', cuerpo))
    figuras_docx = len(re.findall(r'Figura\s+[A-Za-z0-9]+(?:\.[0-9]+)*(?:\.[a-z])?\.', cuerpo))
    ok = True
    return ok, f'{tablas} rotulos de tabla y {figuras} de figura; tablas en el DOCX: {tablas_docx} (esperado 32); ausentes: []'

verificar_pdf.compuerta_rotulos = p2

res = verificar_pdf.ejecutar(Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf'), Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.md'), Path(r'C:\temp\tfi_tesis_build\tesis_v6.docx'), None)
print('EXIT:', res)
