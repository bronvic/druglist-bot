from django.core.management.base import BaseCommand
from django.core.management import call_command
import tempfile
from difflib import unified_diff


class Command(BaseCommand):
    help = "Compare data from website with raw data dump"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="dump file")

    def handle(self, *args, **kwargs):
        new_fname = tempfile.mktemp()
        old_fname = kwargs.get("file", "data_dump")
        call_command("fetch_data", file=new_fname)

        with open(new_fname, "r") as f_new:
            with open(old_fname, "r") as f_old:
                for line in unified_diff(
                    f_old.readlines(),
                    f_new.readlines(),
                    fromfile="old.py",
                    tofile="new.py",
                ):
                    print(line)
