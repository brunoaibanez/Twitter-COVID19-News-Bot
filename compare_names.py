
uno = ['ahorro', 'hacienda', 'bienes', 'reservas', 'riqueza', 'renta', 'miseria', 'escasez',
       'estrechez', 'frugalidad', 'mercado de valores', 'acciones', 'bolsa', 'economia']

dos = ['muerte', 'fallecimiento', 'defuncion', 'obito', 'deceso', 'fin', 'trance', 'transito']

tres = ['recuperados', 'regenerado', 'entonado', 'curado', 'repuesto']

cuatro = ['infectados', 'contagiado', 'contaminado', 'envenenado', 'infecto', 'inficionado']

cinco = ['fronteras', 'limite', 'confin', 'linde', 'divisoria', 'borde', 'contorno', 'separacion']

seis = ['regulamentaciones', 'regulacion', 'ordenacion', 'codificacion', 'legislacion', 'medidas', 'normas', 'leyes']

siete = ['gobiernos', 'gobernacion', 'direccion', 'mando', 'administracion', 'presidencia', 'regencia', 'jefatura', 'gerencia', 'autoridad']


def normalize(key):
    punctuations = '''´!()-[]{};:'"\,<>./?@#$%^&*_~'''
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        key = key.replace(a, b)

    key = key.lower()
    no_punct = ""
    for char in key:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct


def categories(key):
    categories = []
    for word in uno:
        if word in key:
            categories.append(1)

    for word in dos:
        if word in key:
            categories.append(2)

    for word in tres:
        if word in key:
            categories.append(3)

    for word in cuatro:
        if word in key:
            categories.append(4)

    for word in cinco:
        if word in key:
            categories.append(5)

    for word in seis:
        if word in key:
            categories.append(6)

    for word in siete:
        if word in key:
            categories.append(7)

    return categories