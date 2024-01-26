import torch
import torch_xla
from torch.library import Library, impl
from typing import List

xla_pattern_marking_lib = Library("xla_dynamic_broadcast", "DEF")

xla_pattern_marking_lib.define(
    "dynamic_expand(Tensor x, int[] size, Tensor src_tensor, int src_dim, int target_dim) -> Tensor"
)


@impl(xla_pattern_marking_lib, "dynamic_expand", "XLA")
def dynamic_expand_xla(
    x: torch.Tensor,
    size: List[int],
    src_tensor: torch.Tensor,
    src_dim: int,
    target_dim: int,
):
  """Attach pattern boundary metadata to a XLA Tensor.

    Args:
        x: torch.Tensor (On XLA device) - the marked tensor.
        name: str - The name of the pattern, it will be the name of the stablehlo composite op.
        pos: int - Input/output Position of the annotated tensor in the pattern.
        id: str - Unique identifier of the pattern instance.
        is_input: bool - If the annotated tensor is the input to the pattern.
        attr: dict - Attribute of the pattern, it will be passed down to the attribute field
                     in the stablehlo composite.
    """
  return torch_xla._XLAC._xla_dynamic_expand(x, size, src_tensor, src_dim,
                                             target_dim)


@impl(xla_pattern_marking_lib, "dynamic_expand", "CompositeExplicitAutograd")
def dynamic_expand(
    x: torch.Tensor,
    size: List[int],
    src_tensor: torch.Tensor,
    src_dim: int,
    target_dim: int,
):
  size[target_dim] = src_tensor.shape[src_dim]
  return x.expand(*size)


@impl(xla_pattern_marking_lib, "dynamic_expand", "Meta")
def dynamic_expand_meta(
    x: torch.Tensor,
    size: List[int],
    src_tensor: torch.Tensor,
    src_dim: int,
    target_dim: int,
):
  final_size = list(x.shape)
  final_size[target_dim] = src_tensor.shape[src_dim]
  return torch.empty(*final_size, device='meta')