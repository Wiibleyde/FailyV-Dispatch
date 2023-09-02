package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

func InsertDoctor(accountId int, firstName string, lastName string, phoneNumber string, grade string) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfDoctorExist(accountId, firstName, lastName, phoneNumber) {
		return false
	}

	_, err := db.Exec("INSERT INTO doctor (accountId, firstName, lastName, phoneNumber, grade) VALUES (?, ?, ?, ?, ?)", accountId, firstName, lastName, phoneNumber, grade)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func testIfDoctorExist(accountId int, firstName string, lastName string, phoneNumber string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM doctor WHERE accountId = ? AND firstName = ? AND lastName = ? AND phoneNumber = ?", accountId, firstName, lastName, phoneNumber).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func UpdateDoctor(idDoctor int, firstName string, lastName string, phoneNumber string, grade string) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("UPDATE doctor SET firstName = ?, lastName = ?, phoneNumber = ?, grade = ? WHERE id = ?", firstName, lastName, phoneNumber, grade, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetDoctor(accountId int, idDoctor int) Doctor {
	InitDatabase()
	defer CloseDatabase()

	var doctor Doctor
	err := db.QueryRow("SELECT * FROM doctor WHERE accountId = ? AND id = ?", accountId, idDoctor).Scan(&doctor.Id, &doctor.AccountId, &doctor.FirstName, &doctor.LastName, &doctor.PhoneNumber, &doctor.Grade)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return doctor
}

func GetDoctors(accountId int) []Doctor {
	InitDatabase()
	defer CloseDatabase()

	var doctors []Doctor
	rows, err := db.Query("SELECT * FROM doctor WHERE accountId = ?", accountId)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	for rows.Next() {
		var doctor Doctor
		err := rows.Scan(&doctor.Id, &doctor.AccountId, &doctor.FirstName, &doctor.LastName, &doctor.PhoneNumber, &doctor.Grade)
		if err != nil {
			logger.ErrorLogger.Println(err.Error())
		}
		doctors = append(doctors, doctor)
	}
	return doctors
}

func DeleteDoctor(accountId int, idDoctor int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM doctor WHERE accountId = ? AND id = ?", accountId, idDoctor)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}
