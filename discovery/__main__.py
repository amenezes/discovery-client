from cleo import Application
from dotenv import load_dotenv

from discovery import __version__
from discovery.commands import CatalogCommand, HealthCommand, RaftCommand, StatusCommand

load_dotenv()

application = Application("discovery-client", f"{__version__}")
application.add(CatalogCommand())
application.add(StatusCommand())
application.add(RaftCommand())
application.add(HealthCommand())


if __name__ == "__main__":
    application.run()
