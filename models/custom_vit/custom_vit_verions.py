# ======================== VER 1 =============================== #

class ExtendedVisionTransformer(VisionTransformer):
    def __init__(self, *args, **kwargs):
        super(ExtendedVisionTransformer, self).__init__(*args, **kwargs)

        # Define new layers to add on top of the VisionTransformer
        self.jigsaw = nn.Sequential(
        nn.Linear(768, 768),
        nn.ReLU(),
        nn.Linear(768, 768),
        nn.ReLU(),
        nn.Linear(768, 4 * 4)
        )

    def forward(self, x):
        x = super(ExtendedVisionTransformer, self).forward(x)
        x = self.jigsaw(x)

        return x.reshape(-1, 4 * 4)
model = ExtendedVisionTransformer(patch_size=56)


# ======================== VER 2 =============================== #

class ExtendedVisionTransformer(VisionTransformer):
    def __init__(self, *args, **kwargs):
        super(ExtendedVisionTransformer, self).__init__(*args, **kwargs)

        self.jigsaw = nn.Sequential(
            nn.Linear(768, 512),  # First reduction
            nn.ReLU(),
            nn.Linear(512, 256),  # Further reduction
            nn.ReLU(),
            nn.Linear(256, 64),   # Intermediate layer
            nn.ReLU(),
            nn.Linear(64, 16)     # Final reduction to 16 units
        )

    def forward(self, x):
        x = super(ExtendedVisionTransformer, self).forward(x)
        x = self.jigsaw(x)

        return x.reshape(-1, 4 * 4)

model = ExtendedVisionTransformer(patch_size = 56)

