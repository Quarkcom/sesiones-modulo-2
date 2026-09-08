"""Genera tres PDFs sintéticos del guion para comparar señales de retrieval."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

OUT = Path(__file__).resolve().parent / 'data/entrada'
DOCS = {
    'boletin_sap_f110.pdf': (
        'Boletin tecnico SAP F110-031',
        'El error F110-031 aparece durante el proceso automatico de pagos '
        'cuando la sociedad no tiene una configuracion valida para el metodo '
        'de pago seleccionado. Procedimiento: revisar sociedad, validar metodo '
        'de pago y ejecutar nuevamente F110.'),
    'guia_general_errores_sap.pdf': (
        'Guia general de errores SAP',
        'SAP puede producir errores durante procesos financieros y administrativos. '
        'Los fallos de pagos suelen estar relacionados con configuracion, '
        'autorizaciones, datos maestros o parametrizacion del sistema.'),
    'manual_credenciales.pdf': (
        'Procedimiento para restablecer credenciales',
        'Si un usuario pierde acceso a su cuenta debe iniciar el procedimiento de '
        'restablecimiento de credenciales, validar su identidad y definir una nueva '
        'clave de acceso.'),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    for name, (title, body) in DOCS.items():
        path = OUT / name
        document = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=60,
                                     leftMargin=60, topMargin=70, bottomMargin=60,
                                     title=title, author='Laboratorio Sesion 06')
        document.build([Paragraph(title, styles['Title']), Spacer(1, 24),
                        Paragraph(body, styles['BodyText']), Spacer(1, 30),
                        Paragraph('Material sintetico para la demostracion de Retrieval Avanzado. '
                                  'No es documentacion operativa oficial.', styles['Italic'])])
        print('Creado:', path)


if __name__ == '__main__':
    main()
