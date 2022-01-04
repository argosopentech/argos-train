from pathlib import Path

working_dir = Path.cwd()
run_dir = working_dir / "run"


opennmt_checkpoint_prefix = "openmt.model_step_"


class OpenNMTCheckpoint:
    def __init__(self, f):
        """
        Args:
            f (pathlib.Path): OpenNMT checkpoint file
        """
        self.f = f
        self.name = f.name

        # Get checkpoint num
        file_type_postfix = ".pt"
        prefix_found = self.name.find(opennmt_checkpoint_prefix)
        pt_found = self.name.find(file_type_postfix)
        if prefix_found == 0 and pt_found > prefix_found:
            self.num = int(self.name[len(opennmt_checkpoint_prefix) : pt_found])
        else:
            self.num = 0

    def __lt__(self, x):
        return self.num < x.num

    def __str__(self):
        return self.name


opennmt_checkpoints = [
    OpenNMTCheckpoint(f) for f in list(run_dir.glob(opennmt_checkpoint_prefix + "*"))
]

opennmt_checkpoints.sort()
