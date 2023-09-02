package logger

import (
	"log"
	"os"
	"time"
)

var (
	WarningLogger *log.Logger
	InfoLogger    *log.Logger
	ErrorLogger   *log.Logger
	TrafficLogger *log.Logger
)

func getDate() string {
	dt := time.Now()
	return dt.Format("2006-01-02")
}

func InitLogger() {
	// Create logs/ if not exist
	if _, err := os.Stat("logs/"); os.IsNotExist(err) {
		os.Mkdir("logs/", 0777)
	}
	file, err := os.OpenFile("logs/logs-"+getDate()+".log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}

	WarningLogger = log.New(file, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	InfoLogger = log.New(file, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLogger = log.New(file, "ERROR: ", log.Ldate|log.Ltime|log.Lshortfile)
	TrafficLogger = log.New(file, "TRAFFIC: ", log.Ldate|log.Ltime|log.Lshortfile)
}
