class Utils:
    @staticmethod
    def parse_html(text):
        tag_dict = {
            "<b>": "**",
            "</b>": "**",
            "<i>": "_",
            "</i>": "_"
        }
        new_text = text.replace('*', '\*')
        for i, j in tag_dict.items():
            new_text = new_text.replace(i, j)
        return new_text


