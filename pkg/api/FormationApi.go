package api

import (
	"logger"

	"github.com/gofiber/fiber/v2"
)

type AddFormationRequest struct {
	DoctorId  int    `json:"doctor_id"`
	Formation string `json:"formation"`
}

type DeleteFormationRequest struct {
	DoctorId  int    `json:"doctor_id"`
	Formation string `json:"formation"`
}

func addFormationApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Add formation request")
	return c.SendString("Add formation request")
}

func deleteFormationApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Delete formation request")
	return c.SendString("Delete formation request")
}

func getFormationsApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Get formations request")
	return c.SendString("Get formations request")
}
