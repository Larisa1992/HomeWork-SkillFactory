class HTML:
    def __init__(self, output):  # если output не None, то записываем по указанному пти, иначе выводим print
        self.tag = "html"
        self.output = output
        
        self.children = []

    def __enter__(self):
        return self

    def __str__(self):       
        internal = ""
        if (self.children):
            for child in self.children:
                internal += "\n" + str(child)
            return f"<{self.tag}> {internal} \n</{self.tag}>"
        else:
            return f"<{self.tag}> </{self.tag}>"

        # для операции +=
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, type, value, traceback):
        # result = f"<{self.tag}>"
        # for inx, child in enumerate(self.children, 1):
        #     result += "\n" + (" " * inx) + str(child)
        # result += f"\n</{self.tag}>"
        
        if(self.output is None):
            print(self)
        else:
            with open(self.output,"w", encoding = "UTF-8") as file:
               file.write(str(self))

class TopLevelTag(HTML):
    def __init__(self, tag):
        self.tag = tag       
        self.children = []
    
    def __exit__(self, type, value, traceback): pass
        # res = "<%s>" % self.tag
        # for child in self.children:
        #     res += str(child)
        # res += "</%s>" % self.tag
        
# Объекта класса Tag могут быть непарные или быть парные и содержать текст внутри себя.
class Tag(TopLevelTag):
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass:
            self.attributes["class"] = " ".join(klass)

        for attr, value in (kwargs.items()):
            if "_" in attr:
                attr = attr.replace("_", "-") 

            self.attributes[attr] = value
        
    def __str__(self):
        attrs = []                      #список атрибутов в нужном формате ключ = "значение"
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)         #делаем из списка валидную строку с атрибутами тэга (пример:  attrs - id="heading-text" data-bind="not-above")

        if self.children:
            opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "\n<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)

# "test.html"
if __name__ == "__main__":
    with HTML(output = None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body

