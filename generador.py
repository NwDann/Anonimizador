# -*- coding: utf-8 -*-
"""
Generador de Documentos Sintéticos para Cumplimiento de LOPDP (Ecuador)
Este script genera PDFs de contratos y documentos corporativos con datos sensibles
ecuatorianos reales en estructura (Nombres, Cédulas válidas módulo 10, Correos, Direcciones)
y exporta un archivo JSON con el "Ground Truth" (metadatos exactos) para entrenar
modelos de Inteligencia Artificial (DLP / Redacción / NER).

No requiere librerías externas de datos falsos (usa generadores nativos optimizados para Ecuador).
Requiere: pip install reportlab
"""

import os
import json
import random
from datetime import datetime
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle

fake = Faker('es_CO')

CIUDADES_EC = [
    "Guayaquil",
    "Quito",
    "Cuenca",
    "Santo Domingo",
    "Machala",
    "Durán",
    "Manta",
    "Portoviejo",
    "Loja",
    "Ambato",
    "Riobamba",
    "Quevedo",
    "Esmeraldas",
    "Ibarra",
    "Babahoyo",
    "La Libertad",
    "Latacunga",
    "Milagro",
    "Salinas",
    "Tulcán",
    "Puyo",
    "Tena",
    "Nueva Loja",
    "Santa Elena",
    "Montecristi",
    "Bahía de Caráquez",
    "Cayambe",
    "Macas",
    "Jipijapa",
    "Chone",
    "Samborondón",
    "Azogues",
    "Otavalo",
    "Santa Rosa",
    "Huaquillas",
    "Zamora",
    "El Carmen",
    "San Lorenzo",
    "Vinces",
    "La Concordia"
]
EMPRESAS_EC = [
    "Corporación Favorita C.A.",
    "Banco Pichincha C.A.",
    "Corporación El Rosado S.A.",
    "Industrial Pesquera Santa Priscila S.A.",
    "Aurelian Ecuador S.A.",
    "EcuaCorriente S.A.",
    "Pronaca (Procesadora Nacional de Alimentos C.A.)",
    "Dinadec S.A.",
    "Conecel S.A. (Claro Ecuador)",
    "Otecel S.A. (Movistar Ecuador)",
    "Cervecería Nacional CN S.A.",
    "Arca Continental Ecuador",
    "Holcim Ecuador S.A.",
    "Distribuidora Farmacéutica Ecuatoriana Difare S.A.",
    "Tiendas Industriales Asociadas Tía S.A.",
    "Tiendas Tuti",
    "Banco de Guayaquil S.A.",
    "Banco del Pacífico S.A.",
    "Produbanco - Grupo Promerica",
    "Banco Internacional S.A.",
    "Nestlé Ecuador S.A.",
    "La Fabril S.A.",
    "Nirsa S.A. (Atún Real)",
    "Moderna Alimentos S.A.",
    "Kushki",
    "Primax Comercial del Ecuador S.A.",
    "Atimasa S.A.",
    "Petróleos y Servicios PyS C.A.",
    "EP Petroecuador",
    "CNT EP (Corporación Nacional de Telecomunicaciones)",
    "Telconet S.A.",
    "Tesalia CBC",
    "Acería del Ecuador C.A. Adelca",
    "Corporación Quiport (Aeropuerto de Quito)",
    "Dulcafé S.A. (Sweet & Coffee)",
    "Disensa",
    "Pacari Chocolate",
    "Novopan del Ecuador S.A.",
    "Grupo Nobis",
    "Gisis S.A. (Skretting)",
    "Leterago del Ecuador S.A.",
    "Quifatex Ecuador",
    "Corporación Proauto",
    "Danec S.A.",
    "Pharma Brands S.A.",
    "Omni Hospital",
    "Bupa Ecuador",
    "Unacem Ecuador S.A.",
    "Flopec (Flota Petrolera Ecuatoriana)",
    "Grupo Eljuri"
]

prefijo_cedula = random.choice(["C.C.", "C.I.", "Cédula de Identidad", "DNI", "ID", "RUC/C.I."])
prefijo_correo = random.choice(["correo electrónico", "email", "e-mail", "contacto digital"])

# Algoritmo de Cédula Ecuatoriana (Módulo 10)
def generar_cedula_ecuatoriana():
    provincia = random.randint(1, 24)
    tercer_digito = random.randint(0, 5) # 0 a 5 para personas naturales
    secuencial = "".join(str(random.randint(0, 9)) for _ in range(6))
    digits_9 = f"{provincia:02d}{tercer_digito}{secuencial}"
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for i in range(9):
        val = int(digits_9[i]) * coeficientes[i]
        if val > 9: val -= 9
        suma += val
    
    residuo = suma % 10
    digito_verificador = 0 if residuo == 0 else 10 - residuo
    return f"{digits_9}{digito_verificador}"

def generar_entidad_sensible():
    nombre_completo = fake.name()
    cedula = generar_cedula_ecuatoriana()
    correo = fake.ascii_email()
    direccion = f"{fake.street_address()}, {random.choice(CIUDADES_EC)}, Ecuador"
    telefono = fake.numerify("09########")
    salario = f"${random.randint(460, 4500)}.00"
    return {
        "Nombre": nombre_completo,
        "Cedula": cedula,
        "Correo": correo,
        "Direccion": direccion,
        "Telefono": telefono,
        "Salario": salario
    }

# --- GENERADORES DE CONTENIDO LEGAL ---
def plantilla_contrato(data, empresa):
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    return f"""
    <b>CONTRATO INDIVIDUAL DE TRABAJO SUJETO A LA LOPDP</b><br/><br/>
    En {random.choice(CIUDADES_EC)}, con fecha {fecha}, comparecen por una parte <b>{empresa}</b> (EL EMPLEADOR); 
    y por otra parte, <b>{data['Nombre']}</b>, portador(a) de la {prefijo_cedula} <b>{data['Cedula']}</b>, 
    domiciliado(a) en <b>{data['Direccion']}</b>, teléfono <b>{data['Telefono']}</b> y {prefijo_correo} 
    <b>{data['Correo']}</b> (EL TRABAJADOR).<br/><br/>
    <b>PRIMERA - OBJETO:</b> EL TRABAJADOR se compromete a prestar sus servicios lícitos y personales bajo dependencia.<br/><br/>
    <b>SEGUNDA - REMUNERACIÓN:</b> EL EMPLEADOR abonará la cantidad mensual de <b>{data['Salario']}</b>.<br/><br/>
    <b>TERCERA - PRIVACIDAD Y LOPDP:</b> El trabajador autoriza expresamente el tratamiento de sus datos personales 
    aquí contenidos, de conformidad con la Ley Orgánica de Protección de Datos Personales del Ecuador.
    """

def plantilla_nda(data, empresa):
    fecha = datetime.now().strftime("%d/%m/%Y")
    return f"""
    <b>ACUERDO DE NO DIVULGACIÓN (NDA) Y PROTECCIÓN DE DATOS</b><br/><br/>
    Conste por el presente documento, suscrito el {fecha}, el acuerdo de confidencialidad entre <b>{empresa}</b> 
    y el consultor externo <b>{data['Nombre']}</b>, con {prefijo_cedula} <b>{data['Cedula']}</b>, dirección de notificación en 
    <b>{data['Direccion']}</b> y {prefijo_correo} <b>{data['Correo']}</b>.<br/><br/>
    <b>CLÁUSULA DE CONFIDENCIALIDAD:</b> Toda información técnica, financiera o estratégica compartida estará protegida. 
    Las partes se someten a las sanciones de la LOPDP en caso de filtración de bases de datos o información no pública.
    """

# =====================================================================
# 1. COMPROBANTE DE NÓMINA (ROL DE PAGOS)
# Alta densidad de datos sensibles: Sueldo, deducciones IESS y Cuenta Bancaria.
# =====================================================================

def generar_rol_pagos(datos, empresa, styles, estilo_texto):
    sueldo_base = float(datos['Salario'].replace('$', '').replace('.00', ''))
    iess = round(sueldo_base * 0.0945, 2) # Aporte personal IESS Ecuador (9.45%)
    neto = round(sueldo_base - iess, 2)
    cuenta_bancaria = f"22{random.randint(10000000, 99999999)}"
    
    # Agregamos la cuenta al diccionario de metadatos (Ground Truth) dinámicamente
    datos['Cuenta_Bancaria'] = cuenta_bancaria

    elementos = [
        Paragraph("<b>LIQUIDACIÓN DE ROL DE PAGOS INDIVIDUAL</b>", styles['Heading3']),
        Paragraph(f"<b>Colaborador:</b> {datos['Nombre']}<br/><b>C.I.:</b> {datos['Cedula']}<br/><b>Cargo:</b> Especialista de Operaciones", estilo_texto),
        Spacer(1, 15)
    ]

    # Ancho total de página restando márgenes (612 - 100 = 512pt)
    datos_tabla = [
        ["CONCEPTO", "INGRESOS", "DEDUCCIONES"],
        ["Sueldo Unificado", f"${sueldo_base:.2f}", ""],
        ["Bonificación por Cumplimiento", "$50.00", ""],
        ["Aporte IESS (9.45%)", "", f"${iess:.2f}"],
        ["Anticipo de Sueldo", "", "$0.00"],
        ["TOTALES", f"${sueldo_base + 50:.2f}", f"${iess:.2f}"]
    ]

    t = Table(datos_tabla, colWidths=[212, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f4f6f7")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    
    elementos.append(t)
    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph(f"Neto a recibir: <b>${neto + 50:.2f}</b> acreditados a la Cuenta No. <b>{cuenta_bancaria}</b>.", estilo_texto))
    
    return elementos


# =====================================================================
# 2. ACTA DE ENTREGA - RECEPCIÓN DE ACTIVOS (TI / RRHH)
# Documento corporativo estándar. Contiene números de serie y cédulas.
# =====================================================================

def generar_acta_activos(datos, empresa, styles, estilo_texto):
    fecha = datetime.now().strftime("%d/%m/%Y")
    serie_laptop = fake.bothify("S/N: ????-#######")
    imei_cel = fake.bothify("IMEI: 86402##########")
    
    elementos = [
        Paragraph("<b>ACTA DE ENTREGA-RECEPCIÓN DE EQUIPOS CORPORATIVOS</b>", styles['Heading3']),
        Paragraph(f"En Quito, con fecha {fecha}, la gerencia de TI de <b>{empresa}</b> hace entrega formal al custodio <b>{datos['Nombre']}</b>, portador de la {prefijo_cedula} <b>{datos['Cedula']}</b>, de los siguientes activos corporativos:", estilo_texto),
        Spacer(1, 15)
    ]

    tabla_activos = [
        ["CÓDIGO", "DESCRIPCIÓN DEL EQUIPO", "SERIE / SERVICE TAG", "VALOR"],
        ["LPT-042", "Laptop Dell Latitude 5420", serie_laptop, "$1,250.00"],
        ["CEL-109", "Samsung Galaxy A54", imei_cel, "$380.00"],
        ["MNT-881", "Monitor LG 24 pulgadas", fake.bothify('S/N: CN-######'), "$190.00"]
    ]

    t = Table(tabla_activos, colWidths=[80, 182, 170, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    
    elementos.append(t)
    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph("El custodio autoriza el descuento de su liquidación en caso de pérdida, robo o daño negligente del equipo.", estilo_texto))
    
    return elementos


# =====================================================================
# 3. SOLICITUD DE EJERCICIO DE DERECHOS ARCO (Meta-LOPDP)
# Formulario de un cliente pidiendo que eliminen sus datos de la base.
# =====================================================================

def generar_solicitud_lopdp(datos, empresa, styles, estilo_texto):
    opciones_derecho = ["ACCESO", "RECTIFICACIÓN", "ELIMINACIÓN (DERECHO AL OLVIDO)", "OPOSICIÓN"]
    elegido = random.choice(opciones_derecho)

    elementos = [
        Paragraph("<b>FORMULARIO DE EJERCICIO DE DERECHOS - LOPDP (ECUADOR)</b>", styles['Heading3']),
        Paragraph(f"<b>Titular de los datos:</b> {datos['Nombre']}<br/><b>{prefijo_cedula}:</b> {datos['Cedula']}<br/><b>{prefijo_correo}:</b> {datos['Correo']}", estilo_texto),
        Spacer(1, 15)
    ]

    tabla_opciones = [["MARQUE", "DERECHO SOLICITADO SEGÚN CAPÍTULO III DE LA LOPDP"]]
    for op in opciones_derecho:
        marca = "[ X ]" if op == elegido else "[   ]"
        tabla_opciones.append([marca, op])

    t = Table(tabla_opciones, colWidths=[80, 432])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaecee"))
    ]))
    
    elementos.append(t)
    elementos.append(Spacer(1, 15))
    elementos.append(Paragraph(f"<b>Motivo:</b> Solicito de manera inmediata la {elegido.lower()} de mi número telefónico <b>{datos['Telefono']}</b> de su base de datos de telemarketing.", estilo_texto))
    
    return elementos


# =====================================================================
# 4. FACTURA COMERCIAL ELECTRÓNICA (SRI)
# Formato de factura ecuatoriana con IVA actual del 15%.
# =====================================================================

def generar_factura_comercial(datos, empresa, styles, estilo_texto):
    num_factura = f"001-002-{fake.numerify('#########')}"
    clave_acceso = fake.numerify("#" * 49)
    subtotal = float(random.randint(150, 1200))
    iva15 = round(subtotal * 0.15, 2)

    datos['Clave_Acceso_SRI'] = clave_acceso

    elementos = [
        Paragraph(f"<b>FACTURA COMERCIAL</b> | No. {num_factura}", styles['Heading3']),
        Paragraph(f"<font size=7><b>CLAVE DE ACCESO SRI:</b> {clave_acceso}</font>", estilo_texto),
        Spacer(1, 10),
        Paragraph(f"<b>Cliente:</b> {datos['Nombre']}<br/><b>{prefijo_cedula}:</b> {datos['Cedula']}<br/><b>Dirección:</b> {datos['Direccion']}", estilo_texto),
        Spacer(1, 15)
    ]

    detalle_factura = [
        ["CANT", "DESCRIPCIÓN", "P. UNIT", "TOTAL"],
        ["1", "Licenciamiento Anual Software", f"${subtotal:.2f}", f"${subtotal:.2f}"],
        ["", "", "SUBTOTAL:", f"${subtotal:.2f}"],
        ["", "", "IVA 15%:", f"${iva15:.2f}"],
        ["", "", "VALOR TOTAL:", f"${subtotal + iva15:.2f}"]
    ]

    t = Table(detalle_factura, colWidths=[42, 250, 110, 110])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16a085")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))

    elementos.append(t)
    return elementos

# --- MOTOR DE GENERACIÓN BATCH ---
def generar_batch_pdf(cantidad=10, directorio_salida="dataset_sintetico_lopdp"):
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    styles = getSampleStyleSheet()
    estilo_texto = ParagraphStyle('TextoLegal', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, alignment=4)
    
    ground_truth = []
    
    print(f"[*] Generando {cantidad} documentos en '{directorio_salida}'...")
    for i in range(1, cantidad + 1):
        datos = generar_entidad_sensible()
        empresa = random.choice(EMPRESAS_EC)
        tipo = random.choice(["Contrato", "NDA", "RolPagos", "Activos", "SolicitudLOPDP", "Factura"])
        
        filename = f"{tipo}_{i:04d}.pdf"
        filepath = os.path.join(directorio_salida, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
        
        story = [
            Paragraph(f"<b>{empresa}</b>", styles['Heading2']),
            Paragraph("SISTEMA DE GESTIÓN DE CUMPLIMIENTO LOPDP", styles['Normal']),
            Spacer(1, 20)
        ]
        
        if tipo == "Contrato":
            story.append(Paragraph(plantilla_contrato(datos, empresa), estilo_texto))
        elif tipo == "NDA":
            story.append(Paragraph(plantilla_nda(datos, empresa), estilo_texto))
        elif tipo == "RolPagos":
            story.extend(generar_rol_pagos(datos, empresa, styles, estilo_texto))
        elif tipo == "Activos":
            story.extend(generar_acta_activos(datos, empresa, styles, estilo_texto))
        elif tipo == "SolicitudLOPDP":
            story.extend(generar_solicitud_lopdp(datos, empresa, styles, estilo_texto))
        elif tipo == "Factura":
            story.extend(generar_factura_comercial(datos, empresa, styles, estilo_texto))
        
        story.append(Spacer(1, 40))
        story.append(Table([[Paragraph(f"<b>p. {empresa}</b>", estilo_texto), Paragraph(f"<b>{datos['Nombre']}</b><br/>{prefijo_cedula} {datos['Cedula']}", estilo_texto)]], colWidths=[250, 250]))
        
        doc.build(story)
        
        ground_truth.append({
            "archivo_pdf": filename,
            "clase_documento": tipo,
            "entidades_objetivo": datos
        })
        
    archivo_json = os.path.join(directorio_salida, "etiquetas_entrenamiento.json")
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(ground_truth, f, ensure_ascii=False, indent=4)
        
    print(f"[+] Proceso completado exitosamente. Archivo de etiquetas: {archivo_json}")

if __name__ == "__main__":
    generar_batch_pdf(cantidad=150, directorio_salida="dataset_sintetico_lopdp")