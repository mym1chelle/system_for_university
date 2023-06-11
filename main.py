from fastapi import FastAPI, Depends
from data.db_config import get_db_connection

app = FastAPI(
    debug=True,
    title='Module',
    description='API для приложения Module'
)


@app.get('/')
async def add_card(
    conn=Depends(get_db_connection)
):
    # print(conn)
    return {'status': 'success'}