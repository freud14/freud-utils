import argparse


class SplitArgs(argparse.Action):
    """Argparse action for comma-separated list.

    Examples:

        parser.add_argument('--my-int-list', action=SplitArgs, item_type=int, default=[1, 2, 3])
    """

    def __init__(self, *args, item_type=str, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_type = item_type

    def __call__(self, parser, namespace, values, option_string=None):
        values = [] if values == '' else values.split(',')
        setattr(namespace, self.dest, list(map(self.item_type, values)))
