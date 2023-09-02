package api

import (
	"data"
	"logger"

	"github.com/gofiber/fiber/v2"
)

type AddDoctorRequest struct {
	FirstName   string `json:"first_name"`
	LastName    string `json:"last_name"`
	PhoneNumber string `json:"phone_number"`
	Grade       string `json:"grade"`
}

type DeleteDoctorRequest struct {
	DoctorId int `json:"doctor_id"`
}

func addDoctorApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Add doctor request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Add doctor failed")
		return c.Status(401).SendString("Add doctor failed")
	}

	var addDoctorRequest AddDoctorRequest
	err := c.BodyParser(&addDoctorRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	addDoctorCheck := data.InsertDoctor(accountId, addDoctorRequest.FirstName, addDoctorRequest.LastName, addDoctorRequest.PhoneNumber, addDoctorRequest.Grade)
	if addDoctorCheck == false {
		logger.InfoLogger.Println("Add doctor failed")
		return c.Status(401).SendString("Add doctor failed")
	} else {
		logger.InfoLogger.Println("Add doctor success")
		return c.Status(200).SendString("Add doctor success")
	}
}

func getDoctorsApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Get doctors request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Get doctors failed")
		return c.Status(401).SendString("Get doctors failed")
	}

	doctors := data.GetDoctors(accountId)
	if doctors == nil {
		logger.InfoLogger.Println("Get doctors failed")
		return c.Status(401).SendString("Get doctors failed")
	} else {
		logger.InfoLogger.Println("Get doctors success")
		return c.Status(200).JSON(doctors)
	}
}

func deleteDoctorApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Delete doctor request")

	accountId := data.GetAccountIdByUUID(c.Cookies("uuid"))
	if accountId == 0 {
		logger.InfoLogger.Println("Delete doctor failed")
		return c.Status(401).SendString("Delete doctor failed")
	}

	var deleteDoctorRequest DeleteDoctorRequest
	err := c.BodyParser(&deleteDoctorRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	deleteDoctorCheck := data.DeleteDoctor(accountId, deleteDoctorRequest.DoctorId)
	if deleteDoctorCheck == false {
		logger.InfoLogger.Println("Delete doctor failed")
		return c.Status(401).SendString("Delete doctor failed")
	} else {
		logger.InfoLogger.Println("Delete doctor success")
		return c.Status(200).SendString("Delete doctor success")
	}
}
