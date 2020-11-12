from dotenv import load_dotenv

from discovery.commands.catalog import CatalogCommand
from discovery.commands.health import HealthCommand
from discovery.commands.raft import RaftCommand
from discovery.commands.status import StatusCommand

load_dotenv()
