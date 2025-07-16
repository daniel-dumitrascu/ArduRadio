from options import Options
from option import Option

class SetupOptions(Options):
    def __init__(self, args):
        super().__init__()
        self.initiateOptions()
        if args is not None and len(args) > 2:
            self.computeArgs(args)

    def initiateOptions(self):
        self.options[Option.SKIP.value] = 0

    def computeArgs(self, args: list[str]):
        for i in range(2, len(args), 2):
            key = args[i]
            
            if i+1 >= len(args):
                return
        
            value = args[i+1]

            if self.options.get(key) is not None:
                #TODO rewrite this part. Each option should know the type (str, bool, int, etc)
                if key == Option.SKIP.value:
                    try:
                        self.options[key] = int(value)
                    except Exception as e:
                        print(f"Parameter {value} for {key} is invalid!")
                else:
                    self.options[key] = value
