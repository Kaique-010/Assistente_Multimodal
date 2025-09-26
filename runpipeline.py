from setup_django import setup_django

# Configura Django antes de importar modelos
setup_django()

from tools.pipeline import pipeline

pipeline.invoke({})