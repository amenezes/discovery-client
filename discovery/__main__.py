from cleo import Application
from dotenv import load_dotenv

from discovery import __version__
from discovery.commands import CatalogCommand

load_dotenv()

application = Application("discovery-client", f"{__version__}")
application.add(CatalogCommand())


if __name__ == "__main__":
    application.run()
