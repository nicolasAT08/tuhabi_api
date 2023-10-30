auth_table = 'habi_db.auth_user'

def login(cur, user, pwd): 
    query = f"""
            SELECT * FROM {auth_table} au
            WHERE au.username = '{user}'
            AND au.password = '{pwd}'
            AND au.is_staff = 0
            AND au.is_active = 1
            OR au.is_superuser = 1;
            """

    cur.execute(query)
    user = cur.fetchone()

    if not user:
        raise Exception('Invalid credentials')

    access = True

    return access