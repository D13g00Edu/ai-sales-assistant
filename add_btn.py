import os, glob

for fp in glob.glob('c:/Users/diego/Desktop/proyectos/Mlops/frontend/app/**/page.tsx', recursive=True):
    with open(fp, 'r', encoding='utf8') as f:
        content = f.read()
    
    if '/architecture' in content and 'Arquitectura' in content:
        continue

    # Buscar el navbar actions
    if '<div className="navbar-actions">' in content:
        content = content.replace(
            '<div className="navbar-actions">', 
            '<div className="navbar-actions">\n           <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>'
        )
    # Special case for page.tsx where it might use <a>
    elif '<a href="/dashboard" className="btn btn-secondary" id="nav-dashboard">' in content:
        content = content.replace(
            '<a href="/dashboard" className="btn btn-secondary" id="nav-dashboard">',
            '<a href="/architecture" className="btn btn-secondary">Arquitectura</a>\n          <a href="/dashboard" className="btn btn-secondary" id="nav-dashboard">'
        )
    # Upload use case
    elif '<Link href="/" className="btn btn-secondary">Volver al Inicio</Link>' in content:
         content = content.replace(
            '<Link href="/" className="btn btn-secondary">Volver al Inicio</Link>',
            '<Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>\n        <Link href="/" className="btn btn-secondary">Volver al Inicio</Link>'
         )
    elif '<Link href="/dashboard" className="btn btn-secondary">Dashboard</Link>' in content and '<div className="navbar-actions">' not in content:
         content = content.replace(
            '<Link href="/dashboard" className="btn btn-secondary">Dashboard</Link>',
            '<Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>\n        <Link href="/dashboard" className="btn btn-secondary">Dashboard</Link>'
         )

    with open(fp, 'w', encoding='utf8') as f:
        f.write(content)
print('Updated buttons')
