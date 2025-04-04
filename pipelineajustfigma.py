import re
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

# Blocos de substituição para cada dispositivo
STYLESHEET_BLOCKS = {
    'desktop': """  <!-- Ícone da página -->
  <link rel="icon" type="image/png" sizes="32x32" href="{{ static_url }}img/Landingpagev2/rectangle-3370.png">
  <link rel="stylesheet" href="{{ static_url }}css/Desktop_vars.css">
  <link rel="stylesheet" href="{{ static_url }}css/Desktop_style.css">""",

    'mobile': """  <!-- Ícone da página -->
  <link rel="icon" type="image/png" sizes="32x32" href="{{ static_url }}img/Landingpagev2/rectangle-3370.png">
  <link rel="stylesheet" href="{{ static_url }}css/Mobile_vars.css">
  <link rel="stylesheet" href="{{ static_url }}css/Mobile_style.css">""",

    'tablet': """  <!-- Ícone da página -->
  <link rel="icon" type="image/png" sizes="32x32" href="{{ static_url }}img/Landingpagev2/rectangle-3370.png">
  <link rel="stylesheet" href="{{ static_url }}css/Tablet_vars.css">
  <link rel="stylesheet" href="{{ static_url }}css/Tablet_style.css">"""
}


class FileHandler(FileSystemEventHandler):
    def __init__(self, base_path, name_app, scripts):
        self.base_path = base_path
        self.name_app = name_app
        self.scripts = scripts

    def process_html(self, filepath, device_type):
        filepath_destin = os.path.join(self.base_path, "templates", f"{device_type.capitalize()}.html")
        print(f"Processando HTML: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print("Erro ao ler HTML:", e)
            return

        content = re.sub(
            r'src="(?!\{\{ static_url \}\})([^"]+\.(?:png|jpg|jpeg|gif|svg))"',
            r'src="{{ static_url }}img/Landingpagev2/\1"', content)

        content = re.sub(r'<link\s+rel="stylesheet"\s+href="\./vars\.css"\s*>', "", content)

        stylesheet_block = STYLESHEET_BLOCKS.get(device_type, "")
        content = re.sub(r'<link\s+rel="stylesheet"\s+href="\./style\.css"\s*>', stylesheet_block, content)

        content = re.sub(r'Document', self.name_app, content)

        content = re.sub(
            r'url\((?!{{static_url}}img/Landingpagev2/)([\'"]?)([^\'")]+)\1\)',
            r'url(\1{{static_url}}img/Landingpagev2/\2\1)', content
        )

        content = re.sub(
            r'(\s*)</body>\s*</html>',
            rf'\1{self.scripts}\n</body>\n</html>', content, flags=re.IGNORECASE
        )

        try:
            with open(filepath_destin, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"HTML para {device_type} processado com sucesso!")
        except Exception as e:
            print("Erro ao escrever HTML:", e)

    def copy_css(self, filepath):
        filename = os.path.basename(filepath)
        dest = os.path.join(self.base_path, "static", "css", filename)
        try:
            shutil.copy2(filepath, dest)
            print(f"CSS atualizado: {filename}")
        except Exception as e:
            print(f"Erro ao copiar CSS {filename}:", e)

    def on_modified(self, event):
        filepath = os.path.abspath(event.src_path)
        filename = os.path.basename(filepath)

        # HTMLs
        if filename.lower().endswith(".html"):
            for device_type in STYLESHEET_BLOCKS.keys():
                if device_type.capitalize() in filename:
                    self.process_html(filepath, device_type.lower())

        # CSSs
        elif filename.endswith(".css"):
            if any(device in filename for device in ["Desktop", "Mobile", "Tablet"]):
                self.copy_css(filepath)


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    name_app = 'Media Cuts Studio'

    scripts = '''
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>
<script src="{{ static_url }}js/inicializer-carousel.js"></script>
<script src="{{ static_url }}js/ajust-window.js"></script>
<script src="{{ static_url }}js/landingpage-buttons.js"></script>
'''

    paths_to_watch = [
        os.path.join(base_path, "pipelineajustfigma"),
        os.path.join(base_path, "static", "css")
    ]

    handler = FileHandler(base_path, name_app, scripts)
    observer = Observer()

    for path in paths_to_watch:
        observer.schedule(handler, path, recursive=False)
        print(f"Monitorando alterações em: {path}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
