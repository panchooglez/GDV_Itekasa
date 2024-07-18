# settings.py

application = {
    'app': 'main',
    'icon': None,  # Opcional, puedes incluir el icono de tu aplicación
    'background': 'builtin-arrow',  # O una imagen personalizada
    'format': 'UDZO',
    'window': {
        'size': (640, 480),
        'position': (100, 100),
    },
    'icon_size': 128,
    'contents': [
        {
            'x': 140,
            'y': 120,
            'type': 'file',
            'path': 'dist/main/main'
        },
        {
            'x': 500,
            'y': 120,
            'type': 'link',
            'path': '/Applications'
        },
    ],
}
