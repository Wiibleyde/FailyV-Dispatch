package api

import (
	"data"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func InitApi() {
	app := fiber.New()

	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowHeaders: "Origin, Content-Type, Accept",
	}))

	// API status
	app.Get("/", homeApi)
	app.Get("/status", statusApi)

	// API account
	app.Post("/api/login", loginApi)
	app.Post("/api/register", registerApi)

	// API admin
	app.Post("/api/addAdmin", addAdminApi)
	app.Get("/api/admins", getAdminsApi)
	app.Post("/api/deleteAdmin", deleteAdminApi)

	// API doctor
	app.Post("/api/addDoctor", addDoctorApi)
	app.Get("/api/doctors", getDoctorsApi)
	app.Post("/api/deleteDoctor", deleteDoctorApi)

	// API formation TODO
	app.Post("/api/addFormation", addFormationApi)
	app.Get("/api/formations", getFormationsApi)
	app.Post("/api/deleteFormation", deleteFormationApi)

	// API intervention
	app.Post("/api/addIntervention", addInterventionApi)
	app.Get("/api/interventions", getInterventionsApi)
	app.Post("/api/deleteIntervention", deleteInterventionApi)

	app.Listen(":3000")
}

func HasAccess(c *fiber.Ctx) bool {
	uuid := c.Cookies("uuid")
	if data.CheckAccountUUID(uuid) == false {
		return false
	}
	return true
}