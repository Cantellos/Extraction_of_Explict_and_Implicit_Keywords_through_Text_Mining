special_chars = r',;:!<>()[]&?=+\"\'./\\'  

def add_spaces_to_special_chars(text):

    processed_text = ''
    i=0
    lenght=len(text)-1
    
    for char in text:
        if char in special_chars:
            
            #1° special case: first character of the text
            if i ==0:
                if text[i + 1] == ' ' or text[i + 1] in special_chars:
                    processed_text += char
                else:
                    processed_text += front_space(char)  
                    
            #Standard case       
            elif 0 < i < lenght:
                
                #1° case: first character of the line
                if text[i - 1]=='\n':
                    if text[i + 1] == ' ' or text[i + 1] in special_chars:
                        processed_text += char
                    else:
                        processed_text += front_space(char) 
                
                #2° case: the netx character is a special character (3 cases)
                elif text[i + 1] in special_chars:
                    if text[i - 1] in special_chars or text[i - 1] == ' ':
                        processed_text += front_space(char)
                    else:
                        processed_text += both_space(char)
                        
                #3° case: the netx character is a space (3 cases)
                elif text[i + 1] == ' ':
                    if text[i - 1] in special_chars or text[i - 1] == ' ':
                        processed_text += char
                    else: 
                        processed_text += back_space(char)
                        
                #4° case: the netx character is a normal character (3 cases)
                elif text[i - 1] in special_chars or text[i - 1] == ' ':
                    processed_text += front_space(char)
                     
                else:
                    processed_text += both_space(char)    
                
            #2° special case: last character of the text   
            elif i == lenght:
                if text[i - 1] == ' ' or text[i - 1] in special_chars:
                    processed_text += char
                else:
                    processed_text += back_space(char)      
        else:
            processed_text += char
        i += 1
        
    return processed_text

def both_space(char):
    text=''
    text += ' ' + char + ' '
    return text

def front_space(char):
    text=''
    text += char + ' '
    return text

def back_space(char):
    text=''
    text += ' ' + char
    return text