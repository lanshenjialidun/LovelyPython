
#@ignore
#@language python
"""
     Package: Karrigell_QuickForm-1.0.1-alpha
Requirements: Karrigell HTTP Server - http://karrigell.sourceforge.net
 Description: - A simple class that generates html forms with some basic javascript validations. 
              - It is similar to HTML_QuickForm from PEAR (http://pear.php.net).   
      Author: Marcelo Santos Araujo <marcelo@orionlab.net> 
        Date: 23 November 2005
     Version: $Revision Karrigell_QuickForm-1.0.1-alfa
     Credits: Special thanks to Pierre Quentel and Karrigell's developers.
 Contributor: Zoom.Quiet <Zoom.Quiet@gmail.com>
                - Chinese handbook
                - addCheckboxGrp()
                - addRadioList()
                - addCntTextArea()
                - add JSValidation support:
                    addJSValidation()
                    addJSRule()
                    saveJSRule()
"""






class Karrigell_QuickForm:    
    """Simple HTML Forms Generation  - Karrigell_QuickForm"""
    def __init__(self,name,method,action,legend):    	
        """Form name, request method, file target,legend - Karrigell_QuickForm('contact_form','POST','contact.py','form legend')"""
        
        self.form_list = []
        self.css_list = []
        self.js_list =[]
        self.name = name
        self.legend_name = legend
        self.method = method
        self.action = action
        self.jvfxml = ""
        
        self.jvfxmltmpl="""
        <validation-config lang="auto">
        	<form id="%s" show-error="errorMessage" onfail="" 
        	show-type="first">
            %s
        	</form>	
        </validation-config>
        """
        self.jvformtmpl="""
        	<form id="%s" show-error="errorMessage" onfail="" 
        	show-type="first">
            %s
        	</form>
        """
        self.JSvXMLtmpl="""<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE validation-config SYSTEM "validation-config.dtd">
        <validation-config lang="auto">	
        	<form id="%s" show-error="errorMessage" onfail="" 
        	show-type="first">
            %s
        	</form>
        </validation-config>
        """
        self.JSvMXLnode = """
        		<field name="%s" 
        		display-name="%s" onfail="">
        			<depend name="required" />
        		</field>
        """
        self.JSvRules = []
        
        self.form_list.append("""<div>
    <form method='%s' 
    name='%s' 
    action='%s' 
    id='%s' enctype='multipart/form-data'>
    <fieldset><legend>
    <b>%s</b>
    </legend><table>"""%(self.method
                         ,self.name
                         ,self.action
                         ,self.name
                         ,self.legend_name)
                         )
    
    def addElement(self,element,name,options=None):
        """add a form element: text,file,image,submit,reset,header 
            - addElement('text'
                         ,'full_name'
                         ,{'size':20
                           ,'maxlength':'40'})
        available elements: 
        text, checkbox, submit, reset, file,image,header 
        """
        
        if element == 'text':
            size = options['size']
            size = str(size)
            maxlength = options['maxlength']
            maxlength = str(maxlength)
            self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"' size='"+size+"' maxlength='"+maxlength+"'><td></tr>") 
        
           
        
        
        elif element == 'node':
            self.form_list.append(name)
        
        
        
        elif element == 'checkbox':
            self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td> <td valign='top' align='left'>")
            checkbox = ""
            dic_check = options.items()
            for a,b in dic_check:
                checkbox = checkbox + "<input type='checkbox' name='"+name+"' value='"+a+"'>"+"<label><font face=verdana size=2> "+b+"</font></label><br>"
            self.form_list.append(checkbox+"</td>")
            self.form_list.append("</tr>")
        
        elif element == 'submit':
            value = options['value']
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"' value='"+value+"'><td></tr>")	
        
        
        elif element == 'reset':
            value= options['value']
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"' value='"+value+"'></td></tr>")
        
        
        elif element == 'file':
            self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title()+":</b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"'><td></tr>")
        
        elif element == 'image':
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><img src='"+name+"'></td></tr>")
        
        elif element == 'header':
            self.form_list.append("<tr><td align='left' valign='top' colspan='2'><b><center>"+name.title()+"</center></b></td></tr>")
            
    
    def addHtmNode(self,element,name,desc,options=None):
        """add a form element: text,file,image,submit,reset,header 
            - addElement('text'
                         ,'object name'
                         ,'print name'
                         ,{'size':20
                           ,'maxlength':'40'})
        available elements: 
        text, checkbox, submit, reset, file,image,header 
        """
        
        if element == 'text':
            size = options['size']
            size = str(size)
            maxlength = options['maxlength']
            maxlength = str(maxlength)
            htm = """<tr>
            <td align='right' valign='top'>
            <b>%s:</b></td>
            <td valign='top' align='left'>
            <input type='%s' 
                name='%s' 
                size='%s' 
                maxlength='%s'><td>
                </tr>
                """
            self.form_list.append(htm%(desc
                                       ,element
                                       ,name
                                       ,size
                                       ,maxlength)
                                    )
            #name.title().replace('_',' ')
        
        
        
        elif element == 'node':
            self.form_list.append(name)
        
        
        
        elif element == 'checkbox':
            self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td> <td valign='top' align='left'>")
            checkbox = ""
            dic_check = options.items()
            for a,b in dic_check:
                checkbox = checkbox + "<input type='checkbox' name='"+name+"' value='"+a+"'>"+"<label><font face=verdana size=2> "+b+"</font></label><br>"
            self.form_list.append(checkbox+"</td>")
            self.form_list.append("</tr>")
        
        elif element == 'submit':
            value = options['value']
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"' value='"+value+"'><td></tr>")	
        
        
        elif element == 'reset':
            value= options['value']
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"' value='"+value+"'></td></tr>")
        
        
        elif element == 'file':
            self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title()+":</b></td><td valign='top' align='left'><input type='"+element+"' name='"+name+"'><td></tr>")
        
        elif element == 'image':
            self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'><img src='"+name+"'></td></tr>")
        
        elif element == 'header':
            self.form_list.append("<tr><td align='left' valign='top' colspan='2'><b><center>"+name.title()+"</center></b></td></tr>")
            
    
    def addTextArea(self,name,rows,cols):
        """ add a textarea element - addTextArea('message','10','90')""" 
        self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td><td valign='top' align='left'><textarea name='"+name+"' cols='"+cols+"' rows='"+rows+"'></textarea><td></tr>")
    
    
    def addCntTextArea(self,name,desc,content,rows,cols):
        """ add a textarea element with content
            - addTextArea('message','desc',"contents...",'10','90')
        """ 
        self.form_list.append("""<tr>
                <td align='right' valign='top'>
                <b>%s:</b></td>
                <td valign='top' align='left'>
                <textarea name='%s' 
                cols='%s'
                rows='%s'>%s</textarea>
                <td></tr>"""%(desc
                              ,name
                              ,cols
                              ,rows
                              ,content)
                            )
    
    
    def addGroup(self,*t):
        """ add a button group 
        """
        htm = """<input 
            type='%s' 
            name='%s' 
            value='%s'
            class='%s'>
        """
        group = ""
        self.form_list.append("<tr><td align='right' valign='top'><b></b></td><td valign='top' align='left'>")
        for a,b,c,d in t:
            group += htm%(a,b,c,d)
        self.form_list.append(group+"</td></tr>")	
    def addComboBox(self,name,t):
        """ add a combobox element 
        - addComboBox('fruits'
                        ,{'apple':'Apple'
                        ,'pear':'Pear'
                        ,'orange':'Orange'})
        """
        self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td> <td align='left' valign='top'><select name='"+name+"[]'>")
        combo = ""
        t= t.items()
        for a,b in t:
            combo = combo + "<option value='"+a+"'>"+b+"</option>"
        self.form_list.append(combo)
        self.form_list.append("</select></td></tr>")
    
    def addRadioGroup(self,name,value):
    	"""add a radio element export in TABLE
        - addRadioGroup('genre'
                        ,{'male':'Male'
                          ,'female':'Female'})
        """
        self.form_list.append("<tr><td align='right' valign='top'><b>"+name.title().replace('_',' ')+":</b></td> <td valign='top' align='left'>")
    	radio = ""
        t = value.items()
        for a,b in t:
            radio = radio + "<input type='radio' name='"+name+"' value='"+a+"'>"+"<label><font face=verdana size=2>"+b+"</font></label><br>"
        self.form_list.append(radio+"</td>")
        self.form_list.append("</tr>")
    
    
    
            
    def addRadioList(self,name,desc,value,id=""):
    	"""add a radio element export as UL LI group
        - addRadioGroup('name','desc'
                        ,{'male':'Male'
                        ,'female':'Female'})
        """
        htm = """
            <li id='%s'>%s:<b></b>
                <ul id='qlist'>"""
        self.form_list.append(htm%(id,desc))
    	radio = ""
        t = value.items()
        tmpl = """<li>
            <input type='radio' 
            name='%s' 
            value='%s'>  
            <label>%s</label>      
            """        
        for a,b in t:
            radio = radio + tmpl%(name,a,b)
        self.form_list.append(radio+"</ul></li>")
        #self.form_list.append("</tr>")
    
            
    def addRadioLi(self,name,desc,vdict,klist,id=""):
    	"""add a radio element export as UL LI group
            - name 列表名
            - desc 项描述
            - vdict 值字典
            - klist 键列表
        """
        htm = """
            <li id='%s'>%s<b></b>
                <ul>"""
        self.form_list.append(htm%(id,desc))
    	radio = ""
        #t = value.items()
        tmpl = """<li>
            <input type='radio' 
            name='%s' 
            value='%s'
            class='chkrd'>
            <label>%s</label>    
            """        
        for k in klist:
            radio +=tmpl%(name,k,vdict[k])
        self.form_list.append(radio+"</ul></li>")
        #<DIV id='qlist'></DIV>
        #self.form_list.append("</tr>")
    
            
    def addVarRadioList(self,name,desc,value,convert,id=""):
    	"""add a radio element export as UL LI group
        - addRadioGroup('name','desc'
                        ,{'male':'Male'
                        ,'female':'Female'})
        """
        htm = """
            <li id='%s'>%s:<b></b>
                <ul id='qlist'>"""
        self.form_list.append(htm%(id,desc))
    	radio = ""
        t = value.items()
        tmpl = """<li>
            <input type='radio' 
            name='%s' 
            value='%s'
            class='chkrd'>  
            <label>%s</label>      
            """        
        for a,b in t:
            radio = radio + tmpl%(name,convert[a],b)
        self.form_list.append(radio+"</ul></li>")
        #self.form_list.append("</tr>")
    
            
    def addRadioGrp(self,name,desc,value):
    	"""add a radio element in TABLE
        - addRadioGroup('name','desc'
                        ,{'male':'Male'
                        ,'female':'Female'})
        """
        htm = """
            <tr><td align='right' valign='top'>
            <b>%s:</b></td> 
            <td valign='top' align='left'>"""
        self.form_list.append(htm%desc)
    	radio = ""
        t = value.items()
        tmpl = """<input type='radio' 
            name='%s' 
            value='%s'>
            <label>%s</label>
            <br>
            """
        for a,b in t:
            radio = radio + tmpl%(name,a,b)
        self.form_list.append(radio+"</td>")
        self.form_list.append("</tr>")
    
        
    
    def addChkboxGrp(self,name,desc,value):
    	"""add a radio element Export in TABLE
        - addRadioGroup('name','desc'
                        ,{'male':'Male'
                        ,'female':'Female'})
        """
        htm = """
            <tr><td align='right' valign='top'>
            <b>%s:</b></td> 
            <td valign='top' align='left'>"""
        self.form_list.append(htm%desc)
    	radio = ""
        t = value.items()
        tmpl = """<input type='checkbox' 
            name='%s[]' 
            value='%s'>
            <label>%s</label>
            <br>
            """
        for a,b in t:
            radio = radio + tmpl%(name,a,b)
        self.form_list.append(radio+"</td>")
        self.form_list.append("</tr>")
    
        
    
    def showFormList(self):
        """ returns the whole form list """
        return self.form_list
    
    def display(self):
        """ displays the html form"""
        self.form_list.append("</table></fieldset></form></div>")
        self.js_list.append("<script type='text/javascript'>")
        print self.js_list.pop()
        print "function validate_%s(frm){"% self.name
        print """var value='';
                 var errFlag=new Array();
                 var _qfGroups={};
                 _qfMsg='';"""
        for k in self.js_list:
            print k+"\n"
        self.js_list.append("</script>")
        final_js_function = """
            if (_qfMsg != ''){
             _qfMsg = 'Form is not correct!' + _qfMsg;
             _qfMsg = _qfMsg+'<break>Please, checkout instructions above';
             alert(_qfMsg);
             return false;
            }
            return true; }
            """
        print final_js_function.replace("<break>","\\n")
        print self.js_list.pop()
        for c in self.css_list:
            print c+"\n"
        for i in self.form_list:
            print i+"\n"
    
    def export(self):
        """ export the html form code
            so people can do something for them self
        """
        exp = ""
        self.form_list.append("""</table>
    </fieldset></form><textarea 
    id="jsvalidation-framework" rows="27" >%s
    </textarea></div>"""%self.jvfxml)
    
        self.js_list.append("<script type='text/javascript'>")
        exp += self.js_list.pop()
        exp += "function validate_%s(frm){"% self.name
        exp += """var value='';
                 var errFlag=new Array();
                 var _qfGroups={};
                 _qfMsg='';"""
        for k in self.js_list:
            exp += k+"\n"
        self.js_list.append("</script>")
        final_js_function = """
            if (_qfMsg != ''){
             _qfMsg = 'Form is not correct!' + _qfMsg;
             _qfMsg = _qfMsg+'<break>Please, checkout instructions above';
             alert(_qfMsg);
             return false;
            }
            return true; }
            """
        exp += final_js_function.replace("<break>","\\n")
        exp += self.js_list.pop()
        for c in self.css_list:
            exp += c+"\n"
        for i in self.form_list:
            exp += i+"\n"
        return exp
    
    def addStyleSheets(self,t):
        """add a basic stylesheet - simple CSS parameters"""
        css = "<style type='text/css'>textarea { background-color:"+t['bgcolor']+";font-family:"+t['font']+"; font-size:"+t['size']+"px; border-style:solid;border-color:"+t['border-color']+";border-width:1px;} option { background-color:"+t['bgcolor']+";font-family:"+t['font']+";border-style:solid;border-color:"+t['border-color']+";border-width:1px;} input { background-color:"+t['bgcolor']+";font-family:"+t['font']+";border-style:solid;border-color:"+t['border-color']+";border-width:1px;} option { background-color:"+t['bgcolor']+";font-family:"+t['font']+";border-style:solid;border-color:"+t['border-color']+";border-width:1px;} select { background-color:"+t['bgcolor']+";font-family:"+t['font']+";border-style:solid;border-color:"+t['border-color']+";border-width:1px;} td { font-size:"+t['size']+"px; font-family:"+t['font']+"}</style>"
        self.css_list.append(css)
    
    def addRule(self,elem_name,rule_type,message):
        """add a javascript rule in order to validate a form field  
        - addRule('elem_name','required','Name is required!')
        """
        orig = "enctype='multipart/form-data"
        repl = """enctype='multipart/form-data' 
            onsubmit='try { 
                var myValidator = validate_%s; 
                } 
            catch(e) { return true; } 
            return myValidator(this);"""    
        if rule_type == "required":
            begin_form=self.form_list[0].replace(orig
                                         ,repl%self.name)
            self.form_list[0] = begin_form
            js_string = """
            obj = frm.elements['%s'];
            //alert(obj.type);
            value=frm.elements['%s'].value;
            if(value==''&&!errFlag['%s']){
                errFlag['%s']=true;
                _qfMsg=_qfMsg + '<break>- %s';
            }
            """ % (elem_name
                   ,elem_name
                   ,elem_name
                   ,elem_name
                   ,message)    
            js_string = js_string.replace("<break>","\\n")
            self.js_list.append(js_string)
            
        else:
            pass
        
    
    def addJSValidation(self):
        """add a javascript rule in order to validate a form field  
        - addRule('elem_name','required','Name is required!')
        """
        orig = "enctype='multipart/form-data'"
        repl = """
            onsubmit='return doValidate("%s");'
            """ 
        begin_form=self.form_list[0].replace(orig
                                     ,repl%self.name) 
        self.form_list[0] = begin_form
         
        
    
    
    def addJSRule(self,name,message):
        """add a xml rule for javascript checking
        """
        exp = self.JSvMXLnode%(name,message)
        self.JSvRules.append(exp)
        
         
        
    
    
    def saveJSRule(self,xml):
        """exp and save a xml rule for javascript checking
        """
        exp = ""
        for node in self.JSvRules:
            exp+= node
        #exp = self.JSvXMLtmpl%(form,exp)
        #self.jvfxml = self.jvfxmltmpl%(self.name,exp)
        #print self.jvfxml
        open(xml,'w').write(self.JSvXMLtmpl%(self.name,exp))
    
    
    
        
         
        
    
    
    
    

"""
   Overview - Karrigell_QuickForm
   
  p = Karrigell_QuickForm('teste','POST','teste.py')
  p.addElement('text','nome',{'size':80,'maxlength':20})
  p.addElement('text','email',{'size':80,'maxlength':20})
  p.addRule('nome','required','campo nome obrigario!')
  p.addComboBox('combo',{'a':'A','b':'B'})
  p.addCheckBox('fuda',{'a':'Letra A','b':'Letra B'})
  p.addElement('image','python.gif')
  p.addElement('file','foto')
  p.addElement('submit','botao_enviar',{'value':'Enviar A'})
  p.addComboBox('sexo',['Masculino','Masculino'],['Feminino','Feminino'])
  p.addTextArea('mensagem','20','80')
  p.addGroup(["submit","botao_enviar","Enviar"],["reset","botao_limpar","Limpar"])
  p.addStyleSheets({'bgcolor':'lightblue','font':'verdana','border-color':'black'})
  p.display()
 
"""

