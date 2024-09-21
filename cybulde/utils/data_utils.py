from shutil import rmtree
from cybulde.utils.utils import run_shell_command

def get_cmd_to_get_raw_data(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> str:
    """
    Get shell command to download the raw data from dvc store
    Inputs:
    ---------
    version: str
        data version
    data_local_save_dir: str
        where to save the downloaded data locally
    dvc_remote_repo: str,
        dvc repository where the remote data is stored
    dvc_raw_dat_folder: str,
        location where the remote data is stored
    github_user_name: str,
        gituhb user name
    github_access_token: str
        github access token

    Returns
    --------
    str
        shell command to download the raw data
    """
    dvc_remote_repo = "https://github.com/venugudavalli/cybulde-data.git"
    dvc_remote_repo = dvc_remote_repo.replace("https://", "")
    dvc_remote_repo = f"https://{github_user_name}:{github_access_token}@{dvc_remote_repo}"
    command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"
    return command


def get_raw_data_with_version(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> None:
    command = get_cmd_to_get_raw_data(
        version, data_local_save_dir, dvc_remote_repo, dvc_data_folder, github_user_name, github_access_token
    )
    rmtree(data_local_save_dir, ignore_errors=True)
    run_shell_command(command)
