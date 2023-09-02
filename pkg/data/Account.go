package data

import (
	"crypto/sha256"
	"encoding/hex"
	"logger"

	_ "github.com/go-sql-driver/mysql"
)

// Encode a string in sha256 in utf8
func encodeSha256(str string) string {
	h := sha256.New()
	h.Write([]byte(str))
	hashSum := h.Sum(nil)
	hashHex := hex.EncodeToString(hashSum)
	return hashHex
}

func InsertAccount(username string, password string, power int) bool {
	InitDatabase()
	defer CloseDatabase()

	if testIfAccountExist(username) {
		return false
	}

	_, err := db.Exec("INSERT INTO account (username, password, power) VALUES (?, ?, ?)", username, encodeSha256(password), power)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

// Test if the username already exist in the database
func testIfAccountExist(username string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM account WHERE username = ?", username).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

// Test if the username and password match in the database
func CheckAccountLogin(username string, password string) bool {
	InitDatabase()
	defer CloseDatabase()

	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM account WHERE username = ? AND password = ?", username, encodeSha256(password)).Scan(&count)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	if count > 0 {
		return true
	}
	return false
}

func GetAccount(accountId int) Account {
	InitDatabase()
	defer CloseDatabase()

	var account Account
	err := db.QueryRow("SELECT * FROM account WHERE id = ?", accountId).Scan(&account.Id, &account.Username, &account.Password, &account.Power)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return account
}

func GetAccountId(username string, withDefet bool) int {
	if withDefet {
		InitDatabase()
		defer CloseDatabase()
	}

	var accountId int
	err := db.QueryRow("SELECT id FROM account WHERE username = ?", username).Scan(&accountId)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return accountId
}

func DeleteAccount(accountId int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("DELETE FROM account WHERE id = ?", accountId)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func UpdateAccount(accountId int, username string, password string, power int) bool {
	InitDatabase()
	defer CloseDatabase()

	_, err := db.Exec("UPDATE account SET username = ?, password = ?, power = ? WHERE id = ?", username, encodeSha256(password), power, accountId)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return true
}

func GetAdmins() []Account {
	InitDatabase()
	defer CloseDatabase()

	var accounts []Account
	rows, err := db.Query("SELECT * FROM account WHERE power = 10")
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	for rows.Next() {
		var account Account
		err := rows.Scan(&account.Id, &account.Username, &account.Password, &account.Power)
		if err != nil {
			logger.ErrorLogger.Println(err.Error())
		}
		accounts = append(accounts, account)
	}
	return accounts
}