package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertStatus(accountId int, idDoctor int, status string) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfStatusExist(accountId, idDoctor) {
		return false
	}

	_, err := db.Exec("INSERT INTO status (accountId, idDoctor, service, dispatch, sorter, available) VALUES (?, ?, ?, ?, ?, ?)", accountId, idDoctor, false, false, false, false)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfStatusExist(accountId int, idDoctor int) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM status WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func UpdateStatus(accountId int, idDoctor int, service bool, dispatch bool, sorter bool, available bool) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("UPDATE status SET service = ?, dispatch = ?, sorter = ?, available = ? WHERE accountId = ? AND idDoctor = ?", service, dispatch, sorter, available, accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetStatus(accountId int, idDoctor int) Status {
	InitDatabase()
	defer CloseDatabase()

	var status Status
	err := db.QueryRow("SELECT * FROM status WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor).Scan(&status.Id, &status.AccountId, &status.IdDoctor, &status.Service, &status.Dispatch, &status.Sorter, &status.Available)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return status
}

func DeleteStatus(accountId int, idDoctor int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM status WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
