from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class DatasetReaderConfig:
    _target_: str = MISSING
    dataset_dir: str = MISSING
    dataset_name: str = MISSING


@dataclass
class GHCDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.GHCDatasetReader"
    dev_split_ratio: float = MISSING


@dataclass
class JigsawToxicCommentsDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.JigsawToxicCommentsDatasetReader"
    dev_split_ratio: float = MISSING


@dataclass
class TwitterCommentsDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "cybulde.data_processing.dataset_readers.TwitterCommentsDatasetReader"
    dev_split_ratio: float = MISSING
    test_split_ratio: float = MISSING


@dataclass
class DatasetReaderManagerConfig:
    _target_: str = "cybulde.data_processing.dataset_readers.DatasetReaderManager"
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dataset_reader_manager_schema", node=DatasetReaderManagerConfig, group="dataset_reader_manager")
    cs.store(
        name="ghc_dataset_reader_schema", node=GHCDatasetReaderConfig, group="dataset_reader_manager/dataset_reader"
    )
    cs.store(
        name="jtc_dataset_reader_schema",
        node=JigsawToxicCommentsDatasetReaderConfig,
        group="dataset_reader_manager/dataset_reader",
    )
    cs.store(
        name="twt_dataset_reader_schema",
        node=TwitterCommentsDatasetReaderConfig,
        group="dataset_reader_manager/dataset_reader",
    )
