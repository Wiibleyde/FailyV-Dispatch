package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertFormation(accountId int, idDoctor int, surgery bool, psychology bool, inspection bool, traumatology bool, helico1 bool, helico2 bool, sorting bool, ppa bool, firstAid bool) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfFormationExist(accountId, idDoctor) {
		return false
	}

	_, err := db.Exec("INSERT INTO formation (accountId, idDoctor, surgery, psychology, inspection, traumatology, helico1, helico2, sorting, ppa, firstAid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", accountId, idDoctor, surgery, psychology, inspection, traumatology, helico1, helico2, sorting, ppa, firstAid)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfFormationExist(accountId int, idDoctor int) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM formation WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func UpdateFormation(accountId int, idDoctor int, surgery bool, psychology bool, inspection bool, traumatology bool, helico1 bool, helico2 bool, sorting bool, ppa bool, firstAid bool) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("UPDATE formation SET surgery = ?, psychology = ?, inspection = ?, traumatology = ?, helico1 = ?, helico2 = ?, sorting = ?, ppa = ?, firstAid = ? WHERE accountId = ? AND idDoctor = ?", surgery, psychology, inspection, traumatology, helico1, helico2, sorting, ppa, firstAid, accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetFormation(accountId int, idDoctor int) Formation {
	InitDatabase()
	defer CloseDatabase()

	var formation Formation
	err := db.QueryRow("SELECT * FROM formation WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor).Scan(&formation.Id, &formation.AccountId, &formation.IdDoctor, &formation.Surgery, &formation.Psychology, &formation.Inspection, &formation.Traumatology, &formation.Helico1, &formation.Helico2, &formation.Sorting, &formation.PPA, &formation.FirstAid)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return formation
}

func UpdateOneFormation(accountId int, idDoctor int, formation string, value bool) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("UPDATE formation SET "+formation+" = ? WHERE accountId = ? AND idDoctor = ?", value, accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func DeleteFormation(accountId int, idDoctor int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM formation WHERE accountId = ? AND idDoctor = ?", accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
