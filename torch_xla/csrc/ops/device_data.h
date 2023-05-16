#ifndef XLA_TORCH_XLA_CSRC_OPS_DEVICE_DATA_H_
#define XLA_TORCH_XLA_CSRC_OPS_DEVICE_DATA_H_

#include <torch/csrc/lazy/backend/backend_data.h>

#include "third_party/xla_client/computation_client.h"
#include "torch_xla/csrc/ir.h"

namespace torch_xla {

class DeviceData : public XlaNode {
 public:
  DeviceData(std::shared_ptr<torch::lazy::BackendData> data);

  std::string ToString() const override;

  torch::lazy::NodePtr Clone(torch::lazy::OpList operands) const override;

  XlaOpVector Lower(LoweringContext* loctx) const override;

  const std::shared_ptr<torch::lazy::BackendData>& data() const {
    return data_;
  }

  // With SPMD sharding propagation, we need to update the unpartitioned
  // backend data with a partitioned one in the node operands.
  void Assign(std::shared_ptr<torch::lazy::BackendData> data) {
    XLA_CHECK(data->shape() == data_->shape())
        << "Shape mismatch: expected (" << data_->shape().to_string()
        << "), actual (" << data->shape().to_string() << ")";
    data_ = data;
  }

  static DeviceData* Cast(const torch::lazy::Node* node);

 private:
  std::shared_ptr<torch::lazy::BackendData> data_;
};

}  // namespace torch_xla

#endif  // XLA_TORCH_XLA_CSRC_OPS_DEVICE_DATA_H_