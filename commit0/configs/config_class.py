from dataclasses import dataclass


@dataclass
class Commit0Config:
    # shared in all steps
    dataset_name: str
    dataset_split: str

    # clone related
    base_dir: str
    repo_split: str

    # build related
    # which repo to build, all or one repo
    num_workers: int

    # test related
    backend: str
    # which branch to work on
    branch: str
    # timeout for running pytest
    timeout: int