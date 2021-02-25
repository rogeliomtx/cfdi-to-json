class Complex:
    def as_array(self, data, item, klass):
        """
        children: [
            {
                item: [
                    {...},
                    {...},
                ],
            }
        ]
        """
        objects = []
        children = data.get("children")[0]

        items = children.get(item)
        if items:
            for _ in items:
                objects.append(klass(_))

        return objects

    def as_dict(self, data, item, klass):
        """
        children: [
            {item: {}},
            {item: {}},
        ]
        """
        children = data.get("children")

        objects = []
        for _ in children:
            _ = _.get(item)
            objects.append(klass(_))
        return objects

    def get_optional(self, data, item, klass):
        if data.get(item):
            return klass(data.get(item))
        return None

    def get_complex(self, data, item, klass):
        child = data.get("children")[0].get(item)

        if type(child) == list:
            return self.as_array(data, item, klass)
        elif type(child) == dict:
            return self.as_dict(data, item, klass)
        else:
            raise Exception("unsupported")

    def has_children(self, data):
        if type(data) != list:
            return False

        return len(data) > 0
