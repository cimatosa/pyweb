import os
import warnings
from collections import defaultdict
from urllib.parse import quote_plus as url_quote
from urllib.parse import unquote_plus as url_unquote

def get_fields():
    fields = defaultdict(lambda: '')
    for f in os.environ["QUERY_STRING"].split('&'):
        try:
            i = f.index("=")
            fields[url_unquote(f[:i])] = url_unquote(f[i+1:])
        except ValueError:
            pass
    return fields

def web_string(s):
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")

def webprint(s):
    print(web_string(str(s)))

def simple_header(title, css_links = []):
    head = '<!DOCTYPE html>\n<html>\n<head>\n<title>{}</title>\n'.format(title)
    if isinstance(css_links, str):
        css_links = [css_links]
    for cl in css_links:
        head += '<link href="{}" rel="stylesheet" type= "text/css">\n'.format(cl)
    head += "<body>\n"
    print(head)
    
def simple_footer():
    print('\n</body>\n</html>')
    
def _check_value(val, default, options, value_name):
    if val not in options:
        warnings.warn("unknown {} '{}', options are {}, use default {} '{}'".format(value_name, val, options, value_name, default))
        val = default
    return val    

def yes_no_btn_bar(img_yes, img_no, link_yes='', link_no='', width="100%", height="35px", padding="5px", div_class='', btn_class='',
                   layout = 'left', btn_width="65px", btn_padding=10, element_kind='link_img'):
    
    layout = _check_value(layout, 'left', ['left', 'right', 'spread', 'center'], 'layout')    
    if layout == 'right':
        yes_btn_style = "position: absolute; left: 100%; transform: translateX({}%); width: {}; height: {}".format(-100, btn_width, height)
        no_btn_style =  "position: absolute; left: 100%; transform: translateX({}%); width: {}; height: {}".format(-200-btn_padding, btn_width, height)
    elif layout == 'spread':
        yes_btn_style = "position: absolute; left: 33%; transform: translateX(-50%); width: {}; height: {}".format(btn_width, height)
        no_btn_style =  "position: absolute; left: 66%; transform: translateX(-50%); width: {}; height: {}".format(btn_width, height)
    elif layout == 'left':
        yes_btn_style = "position: absolute; left: 0%; width: {}; height: {}".format(btn_width, height)
        no_btn_style =  "position: absolute; left: 0%; transform: translateX({}%); width: {}; height: {}".format(100 + btn_padding, btn_width, height)
    elif layout == 'center':
        yes_btn_style = "position: absolute; left: 50%; transform: translateX({}%); width: {}; height: {}".format(-150-btn_padding, btn_width, height)
        no_btn_style =  "position: absolute; left: 50%; transform: translateX({}%); width: {}; height: {}".format( 50+btn_padding, btn_width, height)

     
        
    
    btns  = '<div style="position: relative; width: {}; height: {}; padding: {}" class="{}">\n'.format(width, height, padding, div_class)
    
    element_kind = _check_value(element_kind, 'link_img', ['link_img', 'input'], 'element_kind')
    if element_kind == 'input':
        btns += '  <input type="image" src="{}" alt="yes" style="{}" class="{}">\n'.format(img_yes, yes_btn_style, btn_class)
    elif element_kind == 'link_img':
        btns += '  <a href="{}"><img src="{}" alt="yes" style="{}" class="{}"></a>\n'.format(link_yes, img_yes, yes_btn_style, btn_class)
        
    btns += '  <a href="{}"><img src="{}" alt="no"  style="{}" class="{}"></a>\n'.format(link_no, img_no, no_btn_style, btn_class)
    btns += '</div>\n'
    print(btns)
    
def input_select(name, options, select_class=''):
    print('<select name="{}" class="{}">'.format(name, select_class))
    for o in options:
        print('<option value="{}">{}</option>'.format(web_string(o), web_string(o)))
    print('</select>')
    
def input_text(labels, names=None, values=None, disabled=None, label_width="25%", field_width="70%", height="35px", 
               input_text_div_class='', input_text_label_class='', input_text_field_class='', layout='left_align'):
    if names is None:
        names = labels

    if (disabled is None) or (disabled == False):
        disabled = [False]*len(labels)
    elif disabled is True:
        disabled = [True]*len(labels)
        
        
    layout = _check_value(layout, 'left_align', ['left_align', 'right_align'], 'layout')
        
    for i in range(len(labels)):
        print('<div class="{}">'.format(input_text_div_class))
        
        style_vert_middle = "position: relative; top:50%"
        
        if layout == 'left_align':
            print('<div style="display: inline-block; width:{}; {}" class="{}">{}</div>'.format(                   label_width, style_vert_middle, input_text_label_class, web_string(labels[i])))
        elif layout == 'right_align':
            print('<div style="display: inline-block; width:{}; text-align: right; {}" class="{}">{}</div>'.format(label_width, style_vert_middle, input_text_label_class, web_string(labels[i])))
        if values is not None:
            v = values[i]
        else:
            v = ''
        
        if disabled[i]:
            dis = 'disabled'
        else:
            dis = ''
        print('<input type="text" name="{}" value="{}" {} style="width:{}; {}" class="{}">'.format(web_string(names[i]), web_string(v), dis, field_width, style_vert_middle, input_text_field_class))
        print('</div>')
        
        
