import os
import unittest
from typing import Callable, Dict, List

import torch
import torch_xla
# from torch._higher_order_ops.while_loop import while_loop, while_loop_dense
# from torch_xla.experimental.fori_loop import while_loop
import torch_xla.experimental.fori_loop
from torch._higher_order_ops.while_loop import while_loop
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_builder as xb

# _TORCH_WHILE_LOOP_OPS = [
#     torch._higher_order_ops.while_loop,
# ]

def _fake_while_loop(cond_fn, body_fn, operands):
    while cond_fn(*operands):
        operands = body_fn(*operands)
    return operands

class WhileLoopTest(unittest.TestCase):

    # def test_while_loop_tpu(self):
    #     def cond_fn(x):
    #         # z = torch.tensor(10, device=xm.xla_device())
    #         return x.sum() <= 10
    #         # return counter < xb.Op.scalar(x.builder(), 10, dtype=xb.Type.S32)

    #     def body_fn(x):
    #         # y = torch.tensor(1, device=xm.xla_device())
    #         return (x+1, )
    #         # next_counter = counter + xb.Op.scalar(counter.builder(), 1, dtype=xb.Type.S32)
    #         # x = x + xb.Op.scalar(x.builder(), 1, dtype=xb.Type.S32)
    #         # return xb.Op.tuple((next_counter, x))

    #     # device = xm.xla_device()
    #     xx = torch.zeros(1) # , dtype=torch.int, device=device)
    #     # res = while_loop(cond_fn, body_fn, (x, ))
    #     res = while_loop(cond_fn, body_fn, (xx, ))
    #     print("while_loop result: ", res)
    #     # expected = _fake_while_loop(cond_fn, body_fn, (x, ))
    #     expected = torch.tensor(11, dtype=torch.int) # , device=device)
    #     print("expected result: ", expected)
    #     self.assertEqual(expected, res[0])

    def test_while_loop_tpu_xla(self):
        def cond_fn(x):
            # z = torch.tensor(10, device=xm.xla_device())
            # return x.sum() <= 10
            return counter < xb.Op.scalar(x.builder(), 10, dtype=xb.Type.S32)

        def body_fn(x):
            # y = torch.tensor(1, device=xm.xla_device())
            # return (x+1, )
            next_counter = counter + xb.Op.scalar(counter.builder(), 1, dtype=xb.Type.S32)
            x = x + xb.Op.scalar(x.builder(), 1, dtype=xb.Type.S32)
            return xb.Op.tuple((next_counter, x))

        # device = xm.xla_device()
        xx = torch.zeros(1, dtype=torch.int, device=device)
        # res = while_loop(cond_fn, body_fn, (x, ))
        res = while_loop(cond_fn, body_fn, (xx, ))
        print("while_loop result: ", res)
        # expected = _fake_while_loop(cond_fn, body_fn, (x, ))
        expected = torch.tensor(11, dtype=torch.int) # , device=device)
        print("expected result: ", expected)
        self.assertEqual(expected, res[0])

if __name__ == '__main__':
  test = unittest.main()
  sys.exit(0 if test.result.wasSuccessful() else 1)