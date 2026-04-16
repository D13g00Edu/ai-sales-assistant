import os, glob

for fp in glob.glob('c:/Users/diego/Desktop/proyectos/Mlops/frontend/app/**/page.tsx', recursive=True):
    with open(fp, 'r', encoding='utf8') as f:
        content = f.read()

    # Si hay algun link y no se ha importado
    if '<Link' in content and 'import Link from' not in content:
        if '"use client";' in content:
            content = content.replace('"use client";', '"use client";\nimport Link from "next/link";')
        elif "'use client';" in content:
            content = content.replace("'use client';", "'use client';\nimport Link from 'next/link';")
        else:
            content = "import Link from 'next/link';\n" + content
        with open(fp, 'w', encoding='utf8') as f:
            f.write(content)

print('Imports checkados.')
