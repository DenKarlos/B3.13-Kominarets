# Комментарии писал на английском, который у меня не супер, но эта практика лучше.
# My English is not so good, but I tried to write correct comments by English.
# It's final job to B3 module in SkillFactory online-school by "full-stack web-developer on Python" direction
# That job done by Kominarets Denis - student of PWS-27 group

# const - count-size of tab in spaces ' '
TAB_SPACE = 3

# main class
class Tag:
    def __init__(self, tag, attribs={}, is_single=False):
        self.tag = tag #name of a tag
        self.text = "" #text inside tags
        self.attributes = attribs # attributes of tags made with dictionary
        self.tab_count = 0 # this count define padding size
        self.is_single = is_single 
        self.children = [] # in this list we will append our children with help of '+=' operator

    def __enter__(self):
        return self

    # that function define '+=' operator that append child to children list
    def __iadd__(self, other):
        self.children.append(other)
        return self

    # that function will be redefined in class HTML, it is abstract function
    # it responsible for outputting
    def __exit__(self, type, value, traceback):
        pass

    # transform tag class with all information to string and other child-tags with help of recursion 
    # recursion - repetition of the same function(method) in itself
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items(): #turning dictionary to ...
            attrs.append('%s="%s"' % (attribute, value)) # ... sting of ...
        attrs = " ".join(attrs) # ... necessary view

        if self.attributes: #to avoid space " " between name of tag and ">" if there are not attributes
            attrs = " " + attrs
        if self.tab_count: #to avoid empty line at the top of document
            spaces = "\n" + " " * TAB_SPACE * self.tab_count #reduction of code because we often use that meaning
        else:
            spaces = ''

        if self.children:
            opening = spaces + "<{}{}>".format(self.tag, attrs)
            internal = "%s" % self.text
            for child in self.children:
                child.tab_count = self.tab_count+1 #increase of whitespaces in children
                internal += str(child) #heart of recurtion, child has type of Tag class or of ancestor class
            if self.tab_count: #to stand close tag (</html>) on new line ...
                ending = spaces + "</%s>" % self.tag
            else:
                ending = "\n" + "</%s>" % self.tag
            return opening + internal + ending #forming of final string and returning
        else: # ... because other tags without  children stand on the same line with open tags
            if self.is_single: # sinle tags can't have children :(
                return spaces + "<{}{}/>".format(self.tag, attrs) #forming of final string and returning
            else:
                return spaces + "<{}{}>{}</{}>".format(self.tag, attrs, self.text, self.tag) #forming of final string and returning

# we can do without that class, but by task we have to use it
class TopLevelTag(Tag):
    pass

# that class define a way of outputting with help of __exit__ method
class HTML(TopLevelTag):
    def __init__(self, output=''):
        self.tag = 'html'
        self.text = ""
        self.attributes = {}
        self.tab_count = 0
        self.is_single = False
        self.children = []
        self.output = output # name of

    # print function launch printing recurtion of children and itself
    def __exit__(self, *erunda): #*erunda - not used params :)
        if self.output: # if self.output is defined by initialisation (look def __init__) we output to file (advisably to html file) ...
            f = open(self.output, 'w')
            print(self, file=f)
            f.close()
        else: # ... another way we output to console
            print(self)

# I've changed a way of setting of params in Classes by comparison with example-code
# that code create html-text
if __name__ == "__main__":
    with HTML("B3-13.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", {"class": "main-text"}) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", {"class": "container container-fluid", "id": "lead"}) as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", {"src": "/icon.png", "data_image": "responsive"}, is_single=True) as img:
                    div += img

                body += div

            doc += body
