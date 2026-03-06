import pymysql

# Allow PyMySQL to stand in for MySQLdb (avoids native build requirements)
pymysql.install_as_MySQLdb()
