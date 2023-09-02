package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertIntervention(accountId int, name string) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("INSERT INTO intervention (accountId, name) VALUES (?, ?)", accountId, name)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetInterventions(accountId int) []Intervention {
	InitDatabase()
	defer CloseDatabase()

	var interventions []Intervention
	rows, err := db.Query("SELECT * FROM intervention WHERE accountId = ?", accountId)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	for rows.Next() {
		var intervention Intervention
		err = rows.Scan(&intervention.Id, &intervention.AccountId, &intervention.Name)
		if err != nil {
			logger.ErrorLogger.Println(err.Error())
		}
		interventions = append(interventions, intervention)
	}
	return interventions
}

func DeleteIntervention(accountId int, idIntervention int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM intervention WHERE accountId = ? AND id = ?", accountId, idIntervention)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
