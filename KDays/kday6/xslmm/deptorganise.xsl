<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <!--
       File:        freemind.xsl
       Version:     0.1
       Description: A XSLT stylesheet to transform mindmap files created with FreeMind (http://freemind.sf.net)
                    into HTML files. The transformation will keep the structure of the files, clouds (with it's colors),
                    icons, internal and external links and the ability to collapse whole subtrees of the document (with
                    JavaScript enabled).
                    The results of the transformation were tested and found to be working in the following browsers:
                    -Internet Explorer 6
                    -Mozilla Firefox 0.9 (should be working with nearly any browser using the Geko engine)
                    -Konqueror
                    -Opera 7
                    Other browsers were not tested, but you should have a good chance of gettting things to work
                    with them.
       Usage:       Use any XSLT-Processor (development was done using xsltproc under Linux) to apply this stylesheet
                    to the FreeMind-file. Copy the result and all the PNG-Files inside the script directory
                    (including the icons-subdir) into a directory of it's own (e.g. on a webserver).
                    Open the HTML-file with a webbrowser.
       Author:      Markus Brueckner <freemind-xsl@slash-me.net>
       License:     BSD license without advertising clause. (see http://www.opensource.org/licenses/bsd-license.php
                     for further details)
  -->

  <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Strict//EN" 
    doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
  <xsl:template match="/">
    <html>
      <head>
      <!-- look if there is any node inside the map (there should never be none, but who knows?) 
           and take its text as the title -->
      <xsl:choose>
        <xsl:when test="/map/node">
          <title><xsl:value-of select="/map/node/@TEXT" /></title>
        </xsl:when>
        <xsl:otherwise>
          <title>FreeMind2HTML Mindmap</title>
        </xsl:otherwise>
      </xsl:choose>
      
      <!-- Stylesheet, generator and some JavaScript for the collapsing of the trees 
      <link rel="stylesheet" type="text/css" href="freemind.css" />
      -->
      <style>
      
      BODY{
          font-size: 92%; color: #333333; 
          text-indent: 1em;  
          margin: 0px;  padding: 0px;
          font-family: Tahoma,SimSun;
          background-color: whitesmoke;
      }
      /*
          border-collapse: collapse ;*/
      H1{ margin: 0px;  padding: 0px;
      }
      TABLE { 
          width: 100%;
          font-size: 96%; 
          color: #444444;}
          
      TH { 
          background-color: #777777;
          color: #efefef;}
      
      TABLE#dept{
          background-color: #efefef;
          }
      TABLE#staff TD{
          font-size: 94%;
          background-color: #ffffff;
          }
      
      div.node { 
        padding-bottom:     1ex;
        padding-left:       2em;
      }
      
      div.cloud { 
        padding-bottom:     1ex;
        padding-left:       2em;
        background-color:   #C0C0FF;
        border-width:       2px;
        border-style:       solid;
        border-color:       #A0A0FF;
      }
      
      div.content { 
        border-width:       1px;
        border-style:   dashed;
        border-color:       #C0C0C0;
      }
      
      img.hideshow { 
        padding-right: 1ex;
      }
      
      img.ilink { 
        border-width: 0px;
        padding-left: 1ex;
      }
      </style>
      
      
      <meta name="generator" content="FreeMind-XSL Stylesheet (see: http://freemind-xsl.dev.slash-me.net/ for details)" />
      
      <script type="text/javascript">
        <![CDATA[
        <!--
             function toggle(id)
             {
                 div_el = document.getElementById(id);
                 img_el = document.getElementById('img'+id);
                 if (div_el.style.display != 'none')
                 {
                    div_el.style.display='none';
                    img_el.src = 'show.png';
                 }
                 else
                 {
                    div_el.style.display='block';
                    img_el.src = 'hide.png';
                 };
             };
         -->
        ]]>
      </script>
      </head>
      <body>
        <!-- choose the first nodes text again as the headline -->
        <h1>
          <xsl:choose>
            <xsl:when test="/map/node">
              <xsl:value-of select="/map/node/@TEXT" />
            </xsl:when>
            <xsl:otherwise>
              FreeMind2HTML Mindmap
            </xsl:otherwise>
          </xsl:choose>
        </h1>
        <xsl:apply-templates />
      </body>
    </html>
  </xsl:template>
  <!-- the template to output for each node -->
  <xsl:template match="node">
  <div>
    <!-- generate a unique ID that can be used to reference this node e.g. from the JavaScript -->
    <xsl:variable name="contentID">
        <xsl:value-of select="generate-id()"/>
    </xsl:variable>
  
    <!-- check whether this node is a cloud... -->
    <xsl:choose>
    <xsl:when test="cloud">
      <!-- ...if yes, check whether it has a special color... -->
      <xsl:choose>
        <xsl:when test="cloud/@COLOR">
          <xsl:attribute name="class">cloud</xsl:attribute>
          <xsl:attribute name="style">background-color: <xsl:value-of select="cloud/@COLOR" /></xsl:attribute>
        </xsl:when>
        <!-- no? Then choose some default color -->
        <xsl:otherwise>
          <xsl:attribute name="class">cloud</xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:attribute name="class">node</xsl:attribute>
    </xsl:otherwise>
    </xsl:choose>
    <!-- check whether this node has any child nodes... -->
    <xsl:choose>
    <xsl:when test="node">
      <!-- ...yes? Then put the "hide" button in front of the text... -->
      <img src="hide.png" class="hideshow" alt="hide">
        <xsl:attribute name="onClick"><![CDATA[toggle("]]><xsl:value-of select="$contentID" /><![CDATA[")]]></xsl:attribute>
        <xsl:attribute name="id">img<xsl:value-of select="$contentID" /></xsl:attribute>
      </img>
    </xsl:when>
    <xsl:otherwise>
      <!-- ...no? Then output the empty leaf icon -->
      <img src="leaf.png" class="hideshow" alt="leaf" />
    </xsl:otherwise>
    </xsl:choose>
    <!-- when there are icons for this node then output the according <img>-tags -->
    
    <xsl:for-each select="icon">
    <img>
      <xsl:attribute name="src">icons/<xsl:value-of select="@BUILTIN" />.png</xsl:attribute>
      <xsl:attribute name="alt"><xsl:value-of select="@BUILTIN" /></xsl:attribute>
    </img>
    </xsl:for-each>
    <!-- check whether this node has a link-ID (for external URLs) -->
    <xsl:choose>
    <xsl:when test="@LINK">
      <a>
        <xsl:attribute name="href">
          <xsl:value-of select="@LINK" />
        </xsl:attribute>
        <xsl:value-of select="@TEXT" />
      </a>
    </xsl:when>
    <xsl:otherwise>
        <xsl:value-of select="@TEXT" />
    <!--Zoomq::050830 add 总人数 -->
        <xsl:for-each select="node">
        <xsl:choose>
            <xsl:when test="@TEXT[.='total']"> 
                (members: <xsl:value-of select="node/@TEXT" /> )
            </xsl:when>
            <xsl:otherwise>    
            </xsl:otherwise>
        </xsl:choose>
        </xsl:for-each>
        
    </xsl:otherwise>
    </xsl:choose>    <!-- check if this node has an ID (for the document internal links) -->
    
    <xsl:if test="@ID">
    <!-- note: as FreeMind sometimes prepends the IDs with an underscore which is not valid
               as the first character in an HTML id, we surround the ID with FM<ID>FM -->
    <a>
      <xsl:attribute name="id">FM<xsl:value-of select="@ID"/>FM</xsl:attribute>
    </a>
    </xsl:if>
    <!-- if there are arrowlinks inside this node (i.e. this node is connected to another node
         in FreeMind using an arrow), then create a document internal link -->
    
    <xsl:for-each select="arrowlink">
    <a>
      <xsl:attribute name="href">#FM<xsl:value-of select="@DESTINATION" />FM</xsl:attribute>
      <img src="ilink.png" alt="Internal Link" class="ilink" />
    </a>
    </xsl:for-each>
    <!-- the content div. This div contains all subnodes of this node. It carries the unique ID
         created in the beginning (which is used to hide this div when necessary). The content node
         is only created if there are any subnodes -->
    <xsl:if test="node">
    <div class="content">
    <xsl:attribute name="id">
      <xsl:value-of select="$contentID" />
    </xsl:attribute>
    
    <xsl:choose>
        <xsl:when test="@TEXT[.='DeptOrgVersion']"> 
            <b>部门组织结构信息图谱 维护记录:</b>
            <UL>
            
            <xsl:for-each select="node">
            <li><xsl:value-of select="@TEXT" /></li>
            </xsl:for-each>
            
            </UL>        </xsl:when>
    
        <xsl:otherwise>    
    
    <!-- 针对部门组织进行专门解析 -->
    <xsl:choose>
        <xsl:when test="node/@TEXT[.='dept'] or node/@TEXT[.='staff']"> 
            <table border="0" id="dept">
            
            <xsl:for-each select="node">
            <xsl:choose>
                <xsl:when test="@TEXT[.='dept']"> 
                <tr>
                <th>CVS</th>
                <td>
                    
                    <xsl:for-each select="node">
                        <xsl:if test="@TEXT[.='name']">
                            <xsl:for-each select="node">
                                <xsl:value-of select="@TEXT" />
                            </xsl:for-each>                        </xsl:if>
                        <xsl:if test="@TEXT[.='cvs']">
                            <xsl:for-each select="node">
                                <xsl:value-of select="@TEXT" />
                            </xsl:for-each>                        </xsl:if>
                    </xsl:for-each>
                </td>
                </tr>    
                </xsl:when>
                <xsl:when test="@TEXT[.='staff']"> 
                <tr>
                <th>staffs</th>
                <td>
                    <table border="0" id="staff">
                    <xsl:for-each select="node">
                    <tr><td>    
                    <!-- 顺序 -->
                    <xsl:value-of select="position()"/>
                            <img>
                            <xsl:attribute name="src">
                            id/<xsl:value-of select="node[@TEXT='mail']/node/@TEXT" />.gif</xsl:attribute>
                        </img>
                    
                    
                        
                        </td><td>
                        <xsl:value-of select="node[@TEXT='level']/node/@TEXT" />
                        </td><td>
                        <xsl:value-of select="@TEXT" />
                        </td><td>
                        <a><xsl:attribute name="href">
                            mailto:<xsl:value-of select="node[@TEXT='mail']/node/@TEXT" />@staff.sina.com.cn
                            </xsl:attribute>
                        <xsl:value-of select="node[@TEXT='mail']/node/@TEXT" />@staff.sina.com.cn
                        </a>
                        </td><td>
                        <xsl:value-of select="node[@TEXT='tel']/node/@TEXT" />
                        </td><td>
                        <xsl:value-of select="node[@TEXT='mobile']/node/@TEXT" />
                        </td><td>
                        <xsl:value-of select="node[@TEXT='bd']/node/@TEXT" />
                        </td>
                    </tr>
                    </xsl:for-each>
                    </table>
                    
                </td>
                </tr>
                </xsl:when>
                <xsl:when test="@TEXT[.='total']"> 
            <!--成员人数-->
                </xsl:when>
            
                <xsl:otherwise>    
                    <xsl:value-of select="@TEXT" />
                </xsl:otherwise>
            </xsl:choose>
            </xsl:for-each>
            
            </table>        </xsl:when>
        <xsl:otherwise>    
            <xsl:apply-templates/>    
        </xsl:otherwise>
    </xsl:choose>
    
        </xsl:otherwise>
    </xsl:choose>
    </div>       
    
    </xsl:if>    
  </div>
  </xsl:template>
  
</xsl:stylesheet>
