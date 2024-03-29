class Args:
    def __init__(self, cfg, batch_size=None, data_path=None, zip=False, cache_mode='part',
                 pretrained=None, resume=None, accumulation_steps=None, use_checkpoint=False,
                 disable_amp=False, amp_opt_level=None, output='output', tag=None,
                 eval=False, throughput=False, local_rank=0, fused_window_process=False,
                 fused_layernorm=False, optim=None, use_jigsaw=False, lambda_jigsaw=0.1, mask_ratio=0.5, opts=None):
        self.cfg = cfg
        self.batch_size = batch_size
        self.data_path = data_path
        self.zip = zip
        self.cache_mode = cache_mode
        self.pretrained = pretrained
        self.resume = resume
        self.accumulation_steps = accumulation_steps
        self.use_checkpoint = use_checkpoint
        self.disable_amp = disable_amp
        self.amp_opt_level = amp_opt_level
        self.output = output
        self.tag = tag
        self.eval = eval
        self.throughput = throughput
        self.local_rank = local_rank
        self.fused_window_process = fused_window_process
        self.fused_layernorm = fused_layernorm
        self.optim = optim
        self.use_jigsaw = use_jigsaw
        self.lambda_jigsaw = lambda_jigsaw
        self.mask_ratio = mask_ratio
        self.opts = opts if opts is not None else []

# Create an instance of Args with the appropriate values
manual_args = Args(
    cfg='/content/jigsaw_swin_base_patch4_window7_224_22kto1k_finetune.yaml',
    pretrained = '/content/drive/MyDrive/data/jigsaw_dl/swin_base_patch4_window7_224_22k.pth'
)
