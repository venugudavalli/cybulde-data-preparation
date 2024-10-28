# from cybulde.config_schemas.config_schema import Config
import os

from pathlib import Path

# import dask
import dask.dataframe as dd

from hydra.utils import instantiate

from cybulde.config_schemas.data_processing.dataset_cleaner_schema import DatasetCleanerManagerConfig
from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import custom_instantiate, get_pickle_config
from cybulde.utils.data_utils import filter_based_on_minimum_number_of_words  # ,get_raw_data_with_version,
from cybulde.utils.io_utils import write_yaml_file

# from cybulde.utils.gcp_utils import access_secret_version
from cybulde.utils.utils import get_logger


def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
) -> dd.core.Series:
    return df_partition["text"].apply(dataset_cleaner_manager) # type: ignore


# original decorator removed @get_config(config_path="../configs", config_name="data_processing_config")
@get_pickle_config(config_path="cybulde/configs/automatically_generated", config_name="data_processing_config") # type: ignore
def process_data(config: DataProcessingConfig) -> None:
    # from omegaconf import OmegaConf
    # print("****config data**********")
    # print(OmegaConf.to_yaml(config))
    # print("****end of config data**********")
    # exit(0)
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    processed_data_save_dir = config.processed_data_save_dir

    if config.dask_cluster._target_ == "dask.distributed.LocalCluster":
        logger.info("Local Processing using Dask LocalCluster...")
        from dask.distributed import LocalCluster

        cluster = LocalCluster(config.dask_cluster) # type: ignore
        client = cluster.get_client() # type: ignore
    else:
        logger.info("Remote Processing on GCP...")
        from dask.distributed import Client

        cluster = custom_instantiate(config.dask_cluster)
        client = Client(cluster) # type: ignore
    try:
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)

        logger.info("Cleaning data ...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")
            )
        )
        logger.info("started computing data ...")
        df = df.compute()
        # dask.compute(df)
        logger.info("Finished computing data ...")

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        logger.info(f"min_nrof_words: {config.min_nrof_words} ..")
        logger.info(f"train_parquet_path: {train_parquet_path}")
        logger.info(f"dev_parquet_path: {dev_parquet_path}")
        logger.info(f"test_parquet_path: {test_parquet_path}")
        logger.info("Filtering rows ...")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df = filter_based_on_minimum_number_of_words(train_df, min_nrof_words=config.min_nrof_words)
        dev_df = filter_based_on_minimum_number_of_words(dev_df, min_nrof_words=config.min_nrof_words)
        test_df = filter_based_on_minimum_number_of_words(test_df, min_nrof_words=config.min_nrof_words)

        logger.info("Filtering finished ...")

        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)

        logger.info("docker image push starting...")
        docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
        docker_info_save_path = os.path.join(processed_data_save_dir, "docker_info.yaml")
        write_yaml_file(docker_info_save_path, docker_info)

        logger.info("docker image push finished...")
        logger.info("data processing finished!")
    finally:
        logger.info("closing dask client and cluster...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data()
