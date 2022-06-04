def create_url(url):
    if url.find("&s=1")==-1:
        url = f"{url}&s=1"
    return url
