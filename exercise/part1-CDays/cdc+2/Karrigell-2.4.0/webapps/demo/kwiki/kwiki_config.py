class Config:

    pass

class fontStyle:
    def __init__(self,name,className,classStyle):
        self.name=name
        self.className=className
        self.classStyle=classStyle

    def __repr__(self):
        return '{ name: "%s", className: "%s", classStyle: "%s"}\n' \
            %(self.name,self.className,self.classStyle)
       
config=Config()

config.fontstyles = [  
  fontStyle(name="Normal",
    className="normal",
    classStyle=""),
  fontStyle(name="Python code", 
    className="python", 
    classStyle="font-family: Courier New; font-size: 12px; background-color: #FFFFCC;  border-width: 1; border-style:solid;")
]
