text = 'As an international student at the University of Maryland, there are specific procedures you must follow when applying for exceptions. Here is some guidance on how you can apply for exceptions as an international student:\n\n1. **Part-Time Authorization**:\n   - If you need to be part-time in a semester due to specific reasons, such as illness, academic difficulties, or being in your final semester, you must receive permission from International Student and Scholar Servthe athe appropriate univthe appropriate university department for guidance.'
import re
import html

def text_processing(text):
    # Pattern to match links in the format [link text](url)
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    
    # Pattern to match bold text in the format **bold text**
    bold_pattern = r'\*\*(.*?)\*\*'
    
    # Pattern to match dashes at the beginning of lines
    dash_pattern = r'^-.'
    
    # Define the replacement function for links
    def replace_with_link(match):
        link_text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}">{link_text}</a>'
    
    # Define the replacement function for bold text
    def replace_with_bold(match):
        bold_text = match.group(1)
        return f'<strong>{bold_text}</strong>'
    
    # Define the replacement function for dashes
    def replace_with_bullet(match):
        return '<li>'
    
    # Use re.sub() to replace the patterns with the appropriate HTML tags
    new_text = re.sub(link_pattern, replace_with_link, text)
    new_text = re.sub(bold_pattern, replace_with_bold, new_text)
    new_text = re.sub(dash_pattern, replace_with_bullet, new_text, flags=re.MULTILINE)
    
    return new_text


def clean_and_convert_to_html(text):

    # text = re.sub(r'^- (.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)

    # Convert Markdown-like bold text to HTML underline
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<u>\1</u>', text)

    # Convert Markdown-like bold text to HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert Markdown-like headings to HTML headings
    text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', text)
    
    # Convert Markdown-like links to HTML links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    # Replace newlines with <br> tags
    text = text.replace('\n', '<br>')
    
    return text

import webbrowser

html = clean_and_convert_to_html(text)

with open('output.html', 'w') as f:
    f.write(html)

webbrowser.open('output.html')

