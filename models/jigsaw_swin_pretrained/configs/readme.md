# configs usage 
```markdown

from jsp.configs.configs import get_config

# -- what it does 
def get_config(args):    
    config = _C.clone()
    update_config(config, args)
    return config
```
