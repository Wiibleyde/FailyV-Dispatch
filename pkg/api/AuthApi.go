package api

import (
	"data"
	"logger"

	"github.com/gofiber/fiber/v2"
)

type RegisterRequest struct {
	Username        string `json:"username"`
	Password        string `json:"password"`
	ConfirmPassword string `json:"conpassword"`
}

type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func registerApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Register request")

	var registerRequest RegisterRequest
	err := c.BodyParser(&registerRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	if registerRequest.Password != registerRequest.ConfirmPassword {
		logger.InfoLogger.Println("Register failed")
		return c.Status(401).SendString("Register failed")
	}

	registerCheck := data.InsertAccount(registerRequest.Username, registerRequest.Password, 1)
	if registerCheck == false {
		logger.InfoLogger.Println("Register failed")
		return c.Status(401).SendString("Register failed")
	} else {
		logger.InfoLogger.Println("Register success")
		return c.Status(200).SendString("Register success")
	}
}

func loginApi(c *fiber.Ctx) error {
	logger.InfoLogger.Println("Login request")

	var loginRequest LoginRequest
	err := c.BodyParser(&loginRequest)
	if err != nil {
		logger.ErrorLogger.Println(err)
		return c.Status(400).SendString("Bad request")
	}

	loginCheck := data.CheckAccountLogin(loginRequest.Username, loginRequest.Password)

	if loginCheck == false {
		logger.InfoLogger.Println("Login failed")
		return c.Status(401).SendString("Login failed")
	} else {
		logger.InfoLogger.Println("Login success")
		uuid := data.SetAccountUUID(loginRequest.Username)
		c.Cookie(&fiber.Cookie{
			Name:     "uuid",
			Value:    uuid,
			HTTPOnly: true,
		})
		return c.Status(200).SendString("Login success")
	}
}
