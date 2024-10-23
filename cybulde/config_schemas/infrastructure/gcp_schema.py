from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class GCPConfig:
    project_id: str = "cybulde-435213"
    zone: str = "europe-west2-b"
    network: str = "default"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="gcp_config_schema", node=GCPConfig)
