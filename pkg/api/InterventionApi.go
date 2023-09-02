package api

import (
	"data"
	"logger"

	"github.com/gofiber/fiber/v2"
)

type AddInterventionRequest struct {
	Name string `json:"name"`
}

type DeleteInterventionRequest struct {
	InterventionId int `json:"intervention_id"`
}

func addInterventionApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Add intervention request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Add intervention failed")
		return c.Status(401).SendString("Add intervention failed")
	}

	var addInterventionRequest AddInterventionRequest
	err := c.BodyParser(&addInterventionRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	addInterventionCheck := data.InsertIntervention(accountId, addInterventionRequest.Name)
	if addInterventionCheck == false {
		logger.InfoLogger.Println("Add intervention failed")
		return c.Status(401).SendString("Add intervention failed")
	} else {
		logger.InfoLogger.Println("Add intervention success")
		return c.Status(200).SendString("Add intervention success")
	}
}

func deleteInterventionApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Delete intervention request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Delete intervention failed")
		return c.Status(401).SendString("Delete intervention failed")
	}

	var deleteInterventionRequest DeleteInterventionRequest
	err := c.BodyParser(&deleteInterventionRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	deleteInterventionCheck := data.DeleteIntervention(accountId, deleteInterventionRequest.InterventionId)
	if deleteInterventionCheck == false {
		logger.InfoLogger.Println("Delete intervention failed")
		return c.Status(401).SendString("Delete intervention failed")
	} else {
		logger.InfoLogger.Println("Delete intervention success")
		return c.Status(200).SendString("Delete intervention success")
	}
}

func getInterventionsApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Get interventions request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Get interventions failed")
		return c.Status(401).SendString("Get interventions failed")
	}

	interventions := data.GetInterventions(accountId)
	if interventions == nil {
		logger.InfoLogger.Println("Get interventions failed")
		return c.Status(401).SendString("Get interventions failed")
	} else {
		logger.InfoLogger.Println("Get interventions success")
		return c.Status(200).JSON(interventions)
	}
}
