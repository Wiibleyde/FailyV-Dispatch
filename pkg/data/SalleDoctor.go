package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertSalleDoctor(accountId int, idDoctor int, idSalle int) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfSalleDoctorExist(accountId, idDoctor, idSalle) {
		return false
	}

	_, err := db.Exec("INSERT INTO salleDoctor (accountId, idDoctor, idSalle) VALUES (?, ?, ?)", accountId, idDoctor, idSalle)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfSalleDoctorExist(accountId int, idDoctor int, idSalle int) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM salleDoctor WHERE accountId = ? AND idDoctor = ? AND idSalle = ?", accountId, idDoctor, idSalle).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func DeleteSalleDoctor(accountId int, idDoctor int, idSalle int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM salleDoctor WHERE accountId = ? AND idDoctor = ? AND idSalle = ?", accountId, idDoctor, idSalle)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
