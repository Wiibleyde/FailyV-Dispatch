package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertInterventionDoctor(accountId int, idDoctor int, idIntervention int) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfInterventionDoctorExist(accountId, idDoctor, idIntervention) {
		return false
	}

	_, err := db.Exec("INSERT INTO interventionDoctor (accountId, idDoctor, idIntervention) VALUES (?, ?, ?)", accountId, idDoctor, idIntervention)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfInterventionDoctorExist(accountId int, idDoctor int, idIntervention int) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM interventionDoctor WHERE accountId = ? AND idDoctor = ? AND idIntervention = ?", accountId, idDoctor, idIntervention).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func DeleteInterventionDoctor(accountId int, idDoctor int, idIntervention int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM interventionDoctor WHERE accountId = ? AND idDoctor = ? AND idIntervention = ?", accountId, idDoctor, idIntervention)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
