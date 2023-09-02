package data

import (
	"database/sql"
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

const (
	databaseHost     = "localhost"
	databasePort     = "3306"
	databaseUser     = "root"
	databasePassword = ""
	databaseName     = "dispatch"
)

var db *sql.DB

func InitDatabase() bool {
	var err error
	db, err = sql.Open("mysql", databaseUser+":"+databasePassword+"@tcp("+databaseHost+":"+databasePort+")/"+databaseName+"?parseTime=true")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetDatabase() *sql.DB {
	return db
}

func CloseDatabase() bool {
	db.Close()
	return true
}

func InitTables() bool {
	InitDatabase()
	defer CloseDatabase()

	// Create tables
	_, err := db.Exec("CREATE TABLE IF NOT EXISTS account (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), power INT)")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS doctor (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, firstName VARCHAR(255), lastName VARCHAR(255), phoneNumber VARCHAR(255), grade VARCHAR(255))")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS formation (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, idDoctor INT, surgery BOOLEAN, psychology BOOLEAN, inspection BOOLEAN, traumatology BOOLEAN, helico1 BOOLEAN, helico2 BOOLEAN, sorting BOOLEAN, ppa BOOLEAN, firstAid BOOLEAN)")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS status (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, idDoctor INT, service BOOLEAN, dispatch BOOLEAN, sorter BOOLEAN, available BOOLEAN)")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS intervention (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, name VARCHAR(255))")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS interventionDoctor (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, idDoctor INT, idIntervention INT)")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS salle (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, name VARCHAR(255))")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS account_uuid (id INT AUTO_INCREMENT PRIMARY KEY, accountId INT, uuid VARCHAR(255), createdAt DATETIME)")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
