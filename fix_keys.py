import os

# 1. Update schmeas/responses.py
fp_resp = r'c:/Users/diego/Desktop/proyectos/Mlops/backend/app/schemas/responses.py'
with open(fp_resp, 'r', encoding='utf8') as f:
    c = f.read()

c = c.replace('total_sales: float', 'total_ventas: float')
c = c.replace('total_transactions: int', 'total_transacciones: int')
c = c.replace('avg_ticket: float', 'ticket_promedio: float')
c = c.replace('unique_clients: int', 'clientes_unicos: int')

with open(fp_resp, 'w', encoding='utf8') as f:
    f.write(c)

# 2. Update modules/analytics/services.py
fp_srv = r'c:/Users/diego/Desktop/proyectos/Mlops/backend/app/modules/analytics/services.py'
with open(fp_srv, 'r', encoding='utf8') as f:
    srv = f.read()

srv = srv.replace('total_sales', 'total_ventas')
srv = srv.replace('total_transactions', 'total_transacciones')
srv = srv.replace('avg_ticket', 'ticket_promedio')
srv = srv.replace('unique_clients', 'clientes_unicos')

with open(fp_srv, 'w', encoding='utf8') as f:
    f.write(srv)

print("Keys sincronizadas.")
