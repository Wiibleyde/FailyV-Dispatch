package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertSalle(accountId int, name string) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfSalleExist(accountId, name) {
		return false
	}

	_, err := db.Exec("INSERT INTO salle (accountId, name) VALUES (?, ?)", accountId, name)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfSalleExist(accountId int, name string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM salle WHERE accountId = ? AND name = ?", accountId, name).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func DeleteSalle(accountId int, idSalle int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM salle WHERE accountId = ? AND id = ?", accountId, idSalle)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
