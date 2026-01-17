

# DATABASE_URL = "postgresql://postgres:password@localhost:5432/mydb"




# DATABASE_URL = "postgresql://postgres:root@localhost:5432/MyVegiz"

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


