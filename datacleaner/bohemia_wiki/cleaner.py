import pandas as pd
import re

def extract_sections(lines):
    sections = []
    current_section = []
    for line in lines:
        if line.startswith('===') or line.startswith('===='):
            if current_section:
                sections.append('\n'.join(current_section))
                current_section = []
        else:
            current_section.append(line)
    if current_section:
        sections.append('\n'.join(current_section))
    return sections

def clean_special_characters(text):
    text = re.sub(r'#', '', text)  # Remove '#'
    text = re.sub(r'\{\{(.+?)\}\}', '', text)  # Remove '{{ }}'
    return text

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove leading and trailing whitespaces

    sections = extract_sections(cleaned_lines)

    data = []
    for section in sections:
        title = re.search(r'^==(.+)==$', section, re.MULTILINE)
        if title:
            title = title.group(1).strip()
        else:
            title = 'Untitled'
        
        content = re.sub(r'^==(.+)==$', '', section, flags=re.MULTILINE).strip()
        content = clean_special_characters(content)
        data.append([title, content])

    df = pd.DataFrame(data, columns=['Title', 'Content'])

    df.to_csv(output_file, index=False)

# Usage:
input_file = 'input_data.txt'
output_file = 'output_data.csv'
txt_to_csv(input_file, output_file)
