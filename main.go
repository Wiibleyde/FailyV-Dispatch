package main

import (
	"data"
	"logger"
	"api"
)

func main() {
	logger.InitLogger()
	logger.InfoLogger.Println("Starting program")
	data.InitTables()
	go data.RemoveAllExpiredUUID()
	api.InitApi()
}