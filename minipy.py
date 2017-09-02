import ast

import click

import handlers


__all__ = ['main']


def read_source(file_path):
    return open(file_path).read()


@click.command()
@click.argument('file_path')
def main(file_path):
    source = read_source(file_path)
    module = ast.parse(source)
    click.echo(handlers.minify_node(module))


if __name__ == '__main__':
    main()

