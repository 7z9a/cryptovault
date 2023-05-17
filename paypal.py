from fastapi import FastAPI
import paypalrestsdk
import plotly.graph_objects as go

paypalrestsdk.configure({
    "mode": "sandbox",  # Cambia a "live" para producción
    "client_id": "TU_CLIENT_ID",
    "client_secret": "TU_CLIENT_SECRET"
})

app = FastAPI()

@app.get("/balance")
async def get_account_balance():
    balance = paypalrestsdk.Account.get().balance
    return {"balance": balance}

@app.get("/transactions")
async def get_account_transactions():
    transactions = paypalrestsdk.Transaction.all()
    # Procesa las transacciones según tus necesidades y devuelve los datos relevantes
    return {"transactions": transactions}

@app.get("/dashboard")
async def generate_dashboard():
    balance = paypalrestsdk.Account.get().balance
    transactions = paypalrestsdk.Transaction.all()

    # Procesa los datos de saldo y transacciones para el gráfico
    balance_amount = float(balance["value"])  # Saldo como número
    transaction_dates = [t.create_time for t in transactions]  # Fechas de las transacciones
    transaction_amounts = [float(t.amount["total"]) for t in transactions]  # Montos de las transacciones

    # Crea el gráfico utilizando la biblioteca Plotly
    fig = go.Figure(data=[
        go.Bar(x=transaction_dates, y=transaction_amounts, name='Transacciones'),
        go.Indicator(mode='number', value=balance_amount, title='Saldo')
    ])
    fig.update_layout(title='Dashboard de PayPal')

    # Devuelve el gráfico como HTML para mostrarlo en el navegador
    return fig.to_html(include_plotlyjs='cdn')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
