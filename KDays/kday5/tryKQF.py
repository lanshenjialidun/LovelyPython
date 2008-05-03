from Karrigell_QuickForm import Karrigell_QuickForm

p = Karrigell_QuickForm('teste','POST','foo.py','Authentication')
p.addElement('text','login',{'size':20
                       ,'maxlength':40})
p.addElement('text','password',{'size':20
                       ,'maxlength':40})
p.addRule('login','required',"Login is required!")
p.addGroup(["submit","botao_enviar","submit","Send"]
           ,["reset","botao_limpar","reset","Clear"])
p.display()