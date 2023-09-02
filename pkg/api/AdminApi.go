package api

import (
	"data"
	"logger"

	"github.com/gofiber/fiber/v2"
)

type AddAdminRequest struct {
	AccountId int `json:"account_id"`
}

type DeleteAdminRequest struct {
	AccountId int `json:"account_id"`
}

func addAdminApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Add admin request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Add admin failed")
		return c.Status(401).SendString("Add admin failed")
	}

	account := data.GetAccount(accountId)
	if account.Power > 10 {
		logger.InfoLogger.Println("Add admin failed (not enough power)")
		return c.Status(401).SendString("Add admin failed")
	} 

	var addAdminRequest AddAdminRequest
	err := c.BodyParser(&addAdminRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	accountToUpdate := data.GetAccount(addAdminRequest.AccountId)
	if accountToUpdate.Power >= 10 {
		logger.InfoLogger.Println("Add admin failed (already admin)")
		return c.Status(401).SendString("Add admin failed")
	} 
	result := data.UpdateAccount(addAdminRequest.AccountId, accountToUpdate.Username, accountToUpdate.Password, 10)
	if result == false {
		logger.InfoLogger.Println("Add admin failed")
		return c.Status(401).SendString("Add admin failed")
	} else {
		logger.InfoLogger.Println("Add admin success")
		return c.Status(200).SendString("Add admin success")
	}
}

func getAdminsApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Get admins request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Get admins failed")
		return c.Status(401).SendString("Get admins failed")
	}

	account := data.GetAccount(accountId)
	if account.Power > 10 {
		logger.InfoLogger.Println("Get admins failed (not enough power)")
		return c.Status(401).SendString("Get admins failed")
	} 

	admins := data.GetAdmins()
	if admins == nil {
		logger.InfoLogger.Println("Get admins failed")
		return c.Status(401).SendString("Get admins failed")
	} else {
		logger.InfoLogger.Println("Get admins success")
		return c.JSON(admins)
	}
}

func deleteAdminApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Delete admin request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Delete admin failed")
		return c.Status(401).SendString("Delete admin failed")
	}

	account := data.GetAccount(accountId)
	if account.Power > 10 {
		logger.InfoLogger.Println("Delete admin failed (not enough power)")
		return c.Status(401).SendString("Delete admin failed")
	} 

	var deleteAdminRequest DeleteAdminRequest
	err := c.BodyParser(&deleteAdminRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	accountToUpdate := data.GetAccount(deleteAdminRequest.AccountId)
	if accountToUpdate.Power < 10 {
		logger.InfoLogger.Println("Delete admin failed (not admin)")
		return c.Status(401).SendString("Delete admin failed")
	} 
	result := data.UpdateAccount(deleteAdminRequest.AccountId, accountToUpdate.Username, accountToUpdate.Password, 1)
	if result == false {
		logger.InfoLogger.Println("Delete admin failed")
		return c.Status(401).SendString("Delete admin failed")
	} else {
		logger.InfoLogger.Println("Delete admin success")
		return c.Status(200).SendString("Delete admin success")
	}
}