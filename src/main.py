import time
from builder import create_example_document
from jinja_env import jinja_env as env
from utils import (
    generate_pdf,
    run_command,
    tmpdir,
)


def main():
    # with tmpdir() as tmp_dir:
    #     with open(f"{temp_dir}/example.txt", "w") as file:
    #         file.write("This is a temporary file.")
    #     time.sleep(10)

    # output, error, exit_code = run_command("ls -la")
    # print(output)
    # print(error)
    # print(exit_code)

    output = env.render_template(
        "document.tpl",
        skip_empty_lines=True,
        show_meta=True,
        author="John Doe",
        title="Sample Document",
        content="This is some example text.",
    )
    # print(generate_pdf("sample", output))

    # print(generate_pdf("example", create_example_document()))


if __name__ == "__main__":
    main()
