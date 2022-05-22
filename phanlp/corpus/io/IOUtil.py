

class IOUtil:
    @classmethod
    def write_custom_nature(cls, out, custom_nature_collector):
        if not custom_nature_collector:
            return
        out.write((str(-len(custom_nature_collector)) + "\n").encode('utf-8'))
        for nature in custom_nature_collector:
            out.write((nature.to_string() + "\n").encode('utf-8'))
