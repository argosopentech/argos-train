import pathlib
from pathlib import Path

working_dir = Path.cwd()
run_dir = working_dir / "run"


OPENNMT_CHECKPOINT_PREFIX = "openmt.model_step_"


class Checkpoint:
    def __init__(self, f: pathlib.Path):
        """
        Args:
            f (pathlib.Path): OpenNMT checkpoint file
        """
        self.f = f
        self.name = f.name

        # Get checkpoint num
        file_type_postfix = ".pt"
        prefix_found = self.name.find(OPENNMT_CHECKPOINT_PREFIX)
        pt_found = self.name.find(file_type_postfix)
        if prefix_found == 0 and pt_found > prefix_found:
            self.num = int(self.name[len(OPENNMT_CHECKPOINT_PREFIX) : pt_found])
        else:
            self.num = 0

    def __lt__(self, x):
        return self.num < x.num

    def __str__(self):
        return self.name


def get_checkpoints():
    try:

        opennmt_checkpoints = [
            Checkpoint(f) for f in list(run_dir.glob(OPENNMT_CHECKPOINT_PREFIX + "*"))
        ]

        opennmt_checkpoints.sort()

        return opennmt_checkpoints
    except Exception as e:
        print("Argos Train get_checkpoints error")
        print(e)
        return []
