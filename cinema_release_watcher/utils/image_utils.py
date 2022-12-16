import base64


def build_src_for_html(image: bytes, extension: str) -> str:
    return f'data:image/{extension};base64,{base64.b64encode(image).decode()}'
