package data

import (
	"logger"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gofrs/uuid"

	"time"
)

func generateUUID() string {
	uuid, err := uuid.NewV4()
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return uuid.String()
}

func SetAccountUUID(username string) string {
	InitDatabase()
	defer db.Close()

	accountId := GetAccountId(username, false)

	now := getNowTime()

	uuid := generateUUID()
	_, err := db.Exec("INSERT INTO account_uuid (accountId, uuid, createdAt) VALUES (?, ?, ?)", accountId, uuid, now)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return uuid
}

func GetAccountUUID(accountId int) string {
	InitDatabase()
	defer db.Close()

	var uuid string
	err := db.QueryRow("SELECT uuid FROM account_uuid WHERE accountId = ?", accountId).Scan(&uuid)
	if err != nil {
		logger.ErrorLogger.Println(err.Error())
	}
	return uuid
}

func GetAccountIdByUUID(uuid string) int {
	InitDatabase()
	defer db.Close()

	var accountId int

	err := db.QueryRow("SELECT accountId FROM account_uuid WHERE uuid = ?", uuid).Scan(&accountId)
	if err != nil {
		return 0
	}

	var createdAt time.Time
	err = db.QueryRow("SELECT createdAt FROM account_uuid WHERE uuid = ?", uuid).Scan(&createdAt)
	if err != nil {
		return 0
	}

	if time.Now().Sub(createdAt).Hours() > 4 {
		return 0
	} else {
		now := getNowTime()
		_, err := db.Exec("UPDATE account_uuid SET createdAt = ? WHERE uuid = ?", now, uuid)
		if err != nil {
			logger.ErrorLogger.Println(err.Error())
		}
	}

	return accountId
}

func CheckAccountUUID(uuid string) bool {
	InitDatabase()
	defer db.Close()

	var uuidCheck string
	err := db.QueryRow("SELECT uuid FROM account_uuid WHERE uuid = ?", uuid).Scan(&uuidCheck)
	if err != nil {
		return false
	}
	return true
}

func getNowTime() time.Time {
	return time.Now().UTC()
}

func RemoveAllExpiredUUID() bool {
	logger.InfoLogger.Println("Remove all expired UUID")
	InitDatabase()
	defer db.Close()

	for {
		now := getNowTime()

		_, err := db.Exec("DELETE FROM account_uuid WHERE createdAt < ?", now.Add(-4*time.Hour))
		if err != nil {
			logger.ErrorLogger.Println(err.Error())
		}
		time.Sleep(30 * time.Minute)
		return true
	}
}
