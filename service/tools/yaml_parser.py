import os
import yaml


def yaml_to_dict(yaml_file_path):
    """
        yaml to dict
        Args:
            yaml_file_path (str): path of yaml

        Returns:
            _ (dict):
    """
    assert os.path.exists(yaml_file_path)
    with open(yaml_file_path, 'r', encoding='UTF-8') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    print(yaml_to_dict('../test.yaml'))
