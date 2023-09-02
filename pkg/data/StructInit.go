package data

type Account struct {
	Id       int
	Username string
	Password string
	Power    int
}

type AccountUUID struct {
	Id           int
	AccountId    int
	Uuid         string
	CreationDate string
}

type Doctor struct {
	Id          int
	AccountId   int
	FirstName   string
	LastName    string
	PhoneNumber string
	Grade       string
}

type Formation struct {
	Id           int
	AccountId    int
	IdDoctor     int
	Surgery      bool
	Psychology   bool
	Inspection   bool
	Traumatology bool
	Helico1      bool
	Helico2      bool
	Sorting      bool
	PPA          bool
	FirstAid     bool
}

type Status struct {
	Id        int
	AccountId int
	IdDoctor  int
	Service   bool
	Dispatch  bool
	Sorter    bool
	Available bool
}

type Intervention struct {
	Id        int
	AccountId int
	Name      string
}

type InterventionDoctor struct {
	Id             int
	AccountId      int
	IdDoctor       int
	IdIntervention int
}

type Salle struct {
	Id        int
	AccountId int
	Name      string
}

type SalleDoctor struct {
	Id        int
	AccountId int
	IdDoctor  int
	IdSalle   int
}
