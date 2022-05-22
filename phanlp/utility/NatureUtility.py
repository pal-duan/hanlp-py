from corpus.tag.Nature import Nature


class NatureUtility:
    @classmethod
    def covert_string2nature(cls, name, custom_nature_collector=None):
        nature = Nature.from_string(name)
        if nature is None:
            nature = Nature.create(name)
            if custom_nature_collector is not None:
                custom_nature_collector.add(nature)
        return nature
