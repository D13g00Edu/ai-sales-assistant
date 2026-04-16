import os

fp_pipe = r'c:/Users/diego/Desktop/proyectos/Mlops/backend/app/api/v1/pipelines.py'
with open(fp_pipe, 'r', encoding='utf8') as f:
    c = f.read()
c = c.replace('@router.post("/datasets/upload", response_model=UploadPipelineResponse)', '@router.post("", response_model=UploadPipelineResponse)')
with open(fp_pipe, 'w', encoding='utf8') as f:
    f.write(c)

fp_main = r'c:/Users/diego/Desktop/proyectos/Mlops/backend/app/main.py'
with open(fp_main, 'r', encoding='utf8') as f:
    m = f.read()
m = m.replace('app.include_router(pipelines.router, prefix="/api/v1")', 'app.include_router(pipelines.router, prefix="/api/v1/datasets/upload")')
with open(fp_main, 'w', encoding='utf8') as f:
    f.write(m)
print("Rutas corregidas")
