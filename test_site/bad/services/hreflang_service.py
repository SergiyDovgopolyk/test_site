def generate_hreflangs(base_url: str):
    if not base_url.startswith("/"):
        base_url = f"/{base_url}"
    return {
        "en": base_url,
        "fr": f"/fr{base_url}",
        "es": f"/es{base_url}"
    }