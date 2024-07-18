# Gestión de Viviendas

## Descripción

Esta aplicación de escritorio está diseñada para gestionar una lista de viviendas para alquilar o vender. La aplicación permite añadir nuevas viviendas, eliminar viviendas existentes y generar un video en formato MP4 con la información de las viviendas. La aplicación está empaquetada para macOS y se distribuye como un archivo `.dmg`.

## Funcionalidades

- **Ventana Principal**: 
  - Lista de viviendas (a alquilar o vender) en un `Treeview`.
  - Botón para añadir nuevas viviendas.
  - Botón para eliminar viviendas seleccionadas de la lista.
  - Botón para generar un archivo MP4 con la información de las viviendas.
  - Botón para salir de la aplicación.
- **Añadir Nueva Vivienda**: 
  - Ventana para introducir los datos pertinentes de la vivienda.
  - Posibilidad de seleccionar una foto de la vivienda desde el equipo.
  - Guardar la información de la vivienda en un archivo CSV.
- **Eliminar Vivienda**: 
  - Elimina la vivienda seleccionada y actualiza el archivo CSV.
- **Generar Video**:
  - Crea un video en formato MP4 con la información de las viviendas, incluyendo su ubicación, precio y una imagen redimensionada.
  - Incluye una barra de progreso que muestra el avance del proceso de generación del video.

## Requisitos

Para que la aplicación funcione correctamente, deberás tener en tu directorio `HOME` un directorio `.LED` donde copiarás los directorios `assets` y `datos` de este repositorio, el script `preinstall.sh` automatizara este proceso. (Aún estoy aprendiendo a desplegar aplicaciones bien srry)

## Empaquetar la Aplicación con PyInstaller

### 1. Configurar y Empaquetar con PyInstaller

Asegúrate de tener `PyInstaller` instalado:

```sh
pip install pyinstaller
```

Crea el archivo `main.spec` (ya incluido en el repositorio):

```python
# main.spec

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
```

Empaqueta tu aplicación:

```sh
pyinstaller main.spec
```

Esto creará un directorio `dist/main` que contiene tu aplicación empaquetada como un ejecutable independiente.

### 2. Crear el archivo `.dmg`

#### Instalar `dmgbuild`

Instala `dmgbuild` para crear el archivo `.dmg`:

```sh
pip install dmgbuild
```

#### Configurar el archivo `settings.py`

Crea un archivo `settings.py` con la configuración necesaria:

```python
# settings.py

application = {
    'app': 'main',
    'icon': None,
    'background': 'builtin-arrow',
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
```

#### Generar el archivo `.dmg`

Ejecuta `dmgbuild` para crear el archivo `.dmg`:

```sh
dmgbuild -s settings.py "Gestión de Viviendas" GestionViviendas.dmg
```

## Actualización del Directorio `dist`

Para actualizar el contenido del directorio `dist` (en caso de que actualices el código), sigue estos pasos:

1. Realiza los cambios necesarios en tu código fuente.
2. Vuelve a ejecutar `pyinstaller` con el archivo `main.spec`:

   ```sh
   pyinstaller main.spec
   ```

3. Esto regenerará el directorio `dist/main` con los cambios aplicados.

## Crear el Archivo `.dmg`

Para crear un nuevo archivo `.dmg` después de actualizar el directorio `dist`, ejecuta:

```sh
dmgbuild -s settings.py "Gestión de Viviendas" GestionViviendas.dmg
```

## Distribución

Una vez generado el archivo `.dmg`, puedes distribuirlo a los usuarios. Ellos podrán montar el `.dmg` y arrastrar la aplicación a su carpeta de Aplicaciones para instalarla.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.