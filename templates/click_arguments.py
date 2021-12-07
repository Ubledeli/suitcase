import click


@click.command(help="description")
@click.option('--string_arg', help='path')
@click.option('--bool_arg', default=True, help='flag')
@click.option('--int_arg', default=42, help='self explanatory')
def function(**options):
    string = options['string_arg']
    boolean = options['string_arg']
    integer = options['string_arg']
    print(string, boolean, integer)


if __name__ == "__main__":
    cli = click.Group()
    cli.add_command(function)
    cli()
