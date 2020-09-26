from cleo import Application
from discovery import __version__
from discovery.cli.commands import CatalogCommand
from dotenv import load_dotenv

load_dotenv()

application = Application("discovery-client", f"{__version__}")
application.add(CatalogCommand())


if __name__ == "__main__":
    application.run()
