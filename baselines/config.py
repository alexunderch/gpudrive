from networks.basic_ffn import FeedForwardPolicy
from dataclasses import dataclass
import torch


@dataclass
class ExperimentConfig:
    """Configurations for experiments."""

    # General
    device: str = "cuda"

    # Rendering options
    render: bool = False
    render_mode: str = "rgb_array"
    render_freq: int = 1

    # TODO: Logging
    log_dir: str = "logs"

    # Hyperparameters
    policy: torch.nn.Module = FeedForwardPolicy
    seed: int = 42
    n_steps: int = 1028
    batch_size: int = 256
    verbose: int = 0
    total_timesteps: int = 10_000_000