from jinja2 import Environment, FileSystemLoader

from settings import TEMPLATE_DIR


class CustomJinjaEnvironment:
    def __init__(self, template_dir):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            block_start_string="@@",
            block_end_string="@@",
            variable_start_string="@=",
            variable_end_string="=@",
        )
        self._register_custom_filters()

    def _register_custom_filters(self):
        self.env.filters["date"] = self.date
        self.env.filters["default"] = self.default
        self.env.filters["length"] = self.length

    def render_template(self, template_name, skip_empty_lines=False, **kwargs):
        template = self.env.get_template(template_name)
        output = template.render(**kwargs)
        if skip_empty_lines:
            lines = [
                line
                for line
                in output.split("\n")
                if line.strip()
            ]
            output = "\n".join(lines)
        return output

    @staticmethod
    def date(value, format_string):
        return value.strftime(format_string)

    @staticmethod
    def default(value, default_value):
        return value if value else default_value

    @staticmethod
    def length(value):
        return len(value)


jinja_env = CustomJinjaEnvironment(TEMPLATE_DIR)