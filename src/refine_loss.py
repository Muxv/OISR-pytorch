import torch
import torch.nn as nn


class WeightedRefineLoss(nn.Module):
    def __init__(self):
        super(WeightedRefineLoss, self).__init__()
        
    def forward(self, refine_scores, refine_y, weights):
        return weighted_refine_loss(refine_scores, refine_y, weights)

    
def weighted_refine_loss(refine_scores, refine_y, weights, eps=1e-6):
    R, C = refine_scores.size()
    if refine_scores.size() != refine_y.size():
        assert ValueError("scores have different size from y")
    if weights.size() != R:
        assert ValueError("weights's length is wrong")
    scores = torch.clamp(refine_scores, min=eps, max=1)
    ylogx = torch.log(refine_scores) * refine_y
    ylogx_all_cls = torch.sum(ylogx, dim=1)
    loss = torch.sum(weights * ylogx_all_cls) * -1 / R
    return loss