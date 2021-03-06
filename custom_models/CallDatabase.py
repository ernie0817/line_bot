import psycopg2
import os


def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    query = f"""SELECT * FROM order_meal WHERE user_id = %s"""
    cursor.execute(query, (record_list[0],))
    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break

    if not data:
        table_columns = '(user_id, user_name, participate, date)'
        postgres_insert_query = f"""INSERT INTO order_meal {table_columns} VALUES (%s, %s, %s, %s);"""
        cursor.execute(postgres_insert_query, record_list)

    else:
        postgres_update_query = f"""UPDATE order_meal SET user_name = %s, participate = %s, date = %s WHERE user_id = %s"""
        cursor.execute(postgres_update_query, (record_list[1], record_list[2], record_list[3], record_list[0]))
    #
    # # table_columns = '(alpaca_name, training, duration, date)'
    # # postgres_insert_query = f"""INSERT INTO alpaca_training {table_columns} VALUES (%s,%s,%s,%s)"""

    # postgres_insert_query = f"""INSERT INTO order_meal {table_columns} VALUES (%s, %s, %s, %s)"""
    #
    # cursor.execute(postgres_insert_query, record_list)
    conn.commit()
    message = '資料匯入成功!'
    # print(message)

    cursor.close()
    conn.close()

    return message


def line_select_overall(fetchnumber):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM alpaca_training ORDER BY record_no DESC;"""

    cursor.execute(postgres_select_query)
    raw = cursor.fetchmany(int(fetchnumber))
    message = []

    for i in raw:
        message.append((i[0], i[1], i[2], str(i[3])[:-3], str(i[4])))

    cursor.close()
    conn.close()

    return message


def web_select_overall():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM order_meal ORDER BY record_no;"""

    cursor.execute(postgres_select_query)

    table = []
    while True:
        temp = cursor.fetchmany(10)

        if temp:
            table.extend(temp)
        else:
            break

    cursor.close()
    conn.close()

    return table


# Day24
def web_select_specific(condition):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    condition_query = []

    for key, value in condition.items():
        if value:
            condition_query.append(f"{key}={value}")
    if condition_query:
        condition_query = "WHERE " + ' AND '.join(condition_query)
    else:
        condition_query = ''

    postgres_select_query = f"""SELECT * FROM order_meal {condition_query} ORDER BY record_no;"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)

    table = []
    while True:
        temp = cursor.fetchmany(10)

        if temp:
            table.extend(temp)
        else:
            break

    cursor.close()
    conn.close()

    return table
