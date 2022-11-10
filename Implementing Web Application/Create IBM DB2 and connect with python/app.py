import ibm_db

conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dxj24137;PWD=pGm0FgyMqS3Jy4JV",'','')

sql= "SELECT * FROM users"
stmt= ibm_db.exec_immediate(conn,sql)
dictionary= ibm_db.fetch_assoc(stmt)
print(dictionary)
