class Scrapper:
    def __init__(self, base_url, url_kwargs):
        self.base_url = base_url
        self.full_url = base_url + "?" + "&".join([f"{key}={value}" for key, value in url_kwargs.items()])
        for key, value in url_kwargs.items():
            setattr(self, key, value)

    def download(self):
        error_msg = f"Function download() not implemented for {self.__class__.__name__}. Please implement it in a SubClass."
        raise NotImplementedError(error_msg)
