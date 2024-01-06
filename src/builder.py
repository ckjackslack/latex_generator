import os

from settings import IMAGE_DIR


class TexComponent:
    def render(self):
        raise NotImplementedError(
            "render() method must be implemented by subclasses."
        )


class Document:
    def __init__(self):
        self.components = []
        self.packages = set()
        self.custom = []

    def add_packages(self, *packages):
        for package in packages:
            self.packages.add(package)

    def add_custom_preamble(self, key, value):
        self.custom.append((key, value))

    def add_component(self, component):
        if not isinstance(component, TexComponent):
            raise ValueError("Can only add TexComponent instances")
        self.components.append(component)

    def render(self):
        doc = "\\documentclass{article}\n"
        for package in sorted(list(self.packages)):
            doc += f"\\usepackage{{{package}}}\n"
        for entry in self.custom:
            key, value = entry
            doc += f"\\{key}{{{value}}}\n"
        doc += "\\begin{document}\n"
        for component in self.components:
            doc += component.render()
        doc += "\\end{document}"
        return doc


class Image(TexComponent):
    def __init__(self, filepath, caption="", label="", width=None):
        self.filepath = filepath
        self.caption = caption
        self.label = label
        self.width = width if width is not None else "\\textwidth"

    def render(self):
        return f"\\begin{{figure}}[h]\n\\centering\n\\includegraphics[width={self.width}]{{{self.filepath}}}\n\\caption{{{self.caption}}}\n\\label{{{self.label}}}\n\\end{{figure}}\n"


class ListItem(TexComponent):
    def __init__(self, text):
        self.text = text

    def render(self):
        return f"\\item {self.text}\n"


class List(TexComponent):
    def __init__(self, enumerated=False):
        self.enumerated = enumerated
        self.items = []

    def add_item(self, item):
        if isinstance(item, ListItem):
            self.items.append(item)
        else:
            raise ValueError("List can only contain ListItem instances")

    def render(self):
        list_type = "enumerate" if self.enumerated else "itemize"
        content = "".join(item.render() for item in self.items)
        return f"\\begin{{{list_type}}}\n{content}\\end{{{list_type}}}\n"


class Table(TexComponent):
    def __init__(self, headers, align="c"):
        self.headers = headers
        self.align = align
        self.rows = []

    def add_row(self, row):
        if len(row) != len(self.headers):
            raise ValueError("Row length must match header length")
        self.rows.append(row)

    def render(self):
        header_row = " & ".join(self.headers) + " \\\\ \\hline"
        body_rows = "\n".join([" & ".join(row) + " \\\\" for row in self.rows])
        return f"\\begin{{tabular}}{{{'|'.join(self.align for _ in self.headers)}}}\n\\hline {header_row} \n{body_rows}\n\\end{{tabular}}\n"


class MathFormula(TexComponent):
    def __init__(self, formula):
        self.formula = formula

    def render(self):
        return f"\\[{self.formula}\\]\n"


class Paragraph(TexComponent):
    def __init__(self, text):
        self.text = text

    def render(self):
        return f"{self.text}\n\n"


class Section(TexComponent):
    def __init__(self, title):
        self.title = title
        self.content = []

    def add_content(self, content):
        self.content.append(content)

    def render(self):
        section_text = f"\\section{{{self.title}}}\n"
        for item in self.content:
            section_text += item.render()
        return section_text


def create_example_document():
    doc = Document()

    doc.add_packages(
        "graphicx",
    )
    doc.add_custom_preamble("graphicspath", IMAGE_DIR)

    section = Section("Introduction")

    itemized_list = List()
    itemized_list.add_item(ListItem("First item"))
    itemized_list.add_item(ListItem("Second item"))

    table = Table(["Header 1", "Header 2"], align="cc")
    table.add_row(["Cell 1", "Cell 2"])
    table.add_row(["Cell 3", "Cell 4"])

    math_formula = MathFormula("E = mc^2")

    image = Image(
        os.path.join(IMAGE_DIR, "duck.png"),
        caption="Example Image",
        label="img:example",
    )

    section.add_content(Paragraph("This is the first paragraph of the introduction."))
    section.add_content(itemized_list)
    section.add_content(table)
    section.add_content(math_formula)
    section.add_content(image)

    doc.add_component(section)

    return doc.render()
