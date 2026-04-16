import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_data():
    categories = ['Electrónica', 'Hogar', 'Moda', 'Deportes']
    products = {
        'Electrónica': ['Laptop Pro', 'Smartphone X', 'Auriculares BT', 'Monitor 4K'],
        'Hogar': ['Cafetera Arabica', 'Lámpara LED', 'Silla Ergonómica', 'Robot Aspirador'],
        'Moda': ['Camiseta Algodón', 'Zapatillas Run', 'Chaqueta Invierno', 'Reloj Elegante'],
        'Deportes': ['Mancuernas 5kg', 'Mat Yoga', 'Bicicleta Montaña', 'Pelota Fútbol']
    }
    districts = ['Miraflores', 'San Isidro', 'Surco', 'Barranco', 'La Molina']
    clients = ['Juan Perez', 'Maria Garcia', 'Carlos Lopez', 'Ana Martinez', 'Roberto Sanchez', 'Elena Gomez']

    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    for i in range(200):
        fecha = start_date + timedelta(days=random.randint(0, 365))
        categoria = random.choice(categories)
        producto = random.choice(products[categoria])
        distrito = random.choice(districts)
        cliente = random.choice(clients)
        cantidad = random.randint(1, 5)
        precio_unitario = round(random.uniform(10.0, 500.0), 2)
        total_venta = round(cantidad * precio_unitario, 2)

        data.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'producto': producto,
            'categoria': categoria,
            'cliente': cliente,
            'distrito': distrito,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'total_venta': total_venta
        })

    df = pd.DataFrame(data)
    df.to_excel('ventas_test.xlsx', index=False)
    print("✅ Archivo 'ventas_test.xlsx' generado con éxito.")

if __name__ == "__main__":
    generate_sample_data()
