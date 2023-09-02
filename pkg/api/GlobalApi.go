package api

import "github.com/gofiber/fiber/v2"

func homeApi(c *fiber.Ctx) error {
	return c.SendString("Hello, World 👋!")
}

func statusApi(c *fiber.Ctx) error {
	return c.SendString("OK")
}
