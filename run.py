import yaml
from argparse import ArgumentParser
from swebench.harness.constants import (
    MAP_REPO_VERSION_TO_SPECS,
)
from swebench.harness.log_parsers import (
    MAP_REPO_TO_PARSER,
    parse_log_pytest_options
)
from swebench.harness.run_evaluation import main
from swebench.harness.utils import str2bool

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dataset_name", default="princeton-nlp/SWE-bench_Lite", type=str, help="Name of dataset or path to JSON file.")
    parser.add_argument("--split", type=str, default="test", help="Split of the dataset")
    parser.add_argument("--instance_ids", nargs="+", type=str, help="Instance IDs to run (space separated)")
    parser.add_argument("--predictions_path", type=str, help="Path to predictions file - if 'gold', uses gold predictions", required=True)
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of workers (should be <= 75%% of CPU cores)")
    parser.add_argument("--open_file_limit", type=int, default=4096, help="Open file limit")
    parser.add_argument(
        "--timeout", type=int, default=1_800, help="Timeout (in seconds) for running tests for each instance"
        )
    parser.add_argument(
        "--force_rebuild", type=str2bool, default=False, help="Force rebuild of all images"
    )
    parser.add_argument(
        "--cache_level",
        type=str,
        choices=["none", "base", "env", "instance"],
        help="Cache level - remove images above this level",
        default="env",
    )
    # if clean is true then we remove all images that are above the cache level
    # if clean is false, we only remove images above the cache level if they don't already exist
    parser.add_argument(
        "--clean", type=str2bool, default=False, help="Clean images above cache level"
    )
    parser.add_argument("--run_id", type=str, required=True, help="Run ID - identifies the run")
    parser.add_argument("--spec_config", type=str, required=True, help="Spec YAML config file for repositories")
    args = parser.parse_args()

    with open(args.spec_config, 'r') as f:
        spec_config = yaml.safe_load(f)
    delattr(args, 'spec_config')
    for key in spec_config:
        MAP_REPO_VERSION_TO_SPECS.update({
            key: spec_config[key]
        })

    for key in spec_config:
        MAP_REPO_TO_PARSER.update({
            key: parse_log_pytest_options
        })

    main(**vars(args))
