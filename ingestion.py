import sqlite3, csv, collections

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn 

def close_connection(conn):
    """ close the database connection """
    if conn:
        conn.close()

# Column details: (cid, name, type, notnull, dflt_value, pk) shipment
# ----------------------------------------
# (0, 'id', 'INTEGER', 1, None, 1)
# (1, 'product_id', 'INTEGER', 1, None, 0)
# (2, 'quantity', 'INTEGER', 1, None, 0)
# (3, 'origin', 'TEXT', 1, None, 0)
# (4, 'destination', 'TEXT', 1, None, 0)

# Column details: (cid, name, type, notnull, dflt_value, pk) product
# ----------------------------------------
# (0, 'id', 'INTEGER', 1, None, 1)
# (1, 'name', 'TEXT', 1, None, 0)

con = create_connection("shipment_database.db")
cur = con.cursor()

# delete existing product and shipment data to avoid duplicates before ingestion
cur.execute("DELETE FROM shipment")
cur.execute("DELETE FROM product")
con.commit()

# Ingest product data from shipping_data_0.csv and shipping_data_1.csv into the product table
for file_name in ["./data/shipping_data_0.csv", "./data/shipping_data_1.csv"]:
    with open(file_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT OR IGNORE INTO product (name) VALUES (?)",
                (row['product'],)
            )
        con.commit()
close_connection(con)

con = create_connection("shipment_database.db")
cur = con.cursor()

# Ingest data from shipping_data_0.csv into the shipment table
with open("./data/shipping_data_0.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
            (cur.execute("SELECT id FROM product WHERE name = ?", (row['product'],)).fetchone()[0], row['product_quantity'], row['origin_warehouse'], row['destination_store'])
        )
    con.commit()
close_connection(con)

# Aggregate data from shipping_data_1.csv and shipping_data_2.csv before merging into the shipment table

with open("./data/shipping_data_1.csv", "r") as f:
    reader = csv.DictReader(f)
    product_count = collections.defaultdict(int)
    for row in reader:
        product_count[(row['shipment_identifier'],row['product'])] += 1

with open("./data/shipping_data_2.csv", "r") as f:
    reader = csv.DictReader(f)
    shipment_points = {}
    for row in reader:
        shipment_points[row['shipment_identifier']] = [row['origin_warehouse'], row['destination_store']]

con = create_connection("shipment_database.db")
cur = con.cursor()
# Now we get aggregated data inserted into the shipment table
for (shipment_identifier, product), quantity in product_count.items():
    origin, destination = shipment_points[shipment_identifier]
    cur.execute(
        "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
        (cur.execute("SELECT id FROM product WHERE name = ?", (product,)).fetchone()[0], quantity, origin, destination)
    )
con.commit()
close_connection(con)