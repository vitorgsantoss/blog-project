from django.core.exceptions import ValidationError

def validate_image(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError(
            'Tipo de imagem incompátivel! Envie um arquivo PNG.'
        )