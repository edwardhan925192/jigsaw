def build_model(is_pretrain=True):
    import torch.nn as nn
    layernorm = nn.LayerNorm

    model = JigsawSwinTransformer(
        embed_dim= 128,
        depths= [2, 2, 18, 2],
        num_heads = [4, 8, 16, 32],
        window_size = 7,
        drop_path_rate = 0.2
    )
    return model
