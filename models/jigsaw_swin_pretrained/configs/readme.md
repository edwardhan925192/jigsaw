# configs usage 
```markdown

from jigsaw.models.jigsaw_swin_pretrained.configs.configs import get_config

# -- what it does 
def get_config(args):    
    config = _C.clone()
    update_config(config, args)
    return config
```
