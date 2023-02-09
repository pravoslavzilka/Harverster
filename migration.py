from database import db_session
from models import *

a = User("Admin", "admin@localhost")
a.set_password("heslo")

db_session.add(a)


co1 = Coordinator("Jožo", "jozo@localhost", "+421 956 456 123")
co1.set_password("heslo")

co2 = Coordinator("Peter", "peter@localhost", "+421 741 357 693")
co2.set_password("heslo")

db_session.add(co1)
db_session.add(co2)


r1 = Region()
r1.name = "Berehiv district"

r2 = Region()
r2.name = "Mukachevo district"

db_session.add(r2)
db_session.add(r1)

h1 = Hub()
h1.institution = "Perekrestok boarding school"
h1.address = "Perekhrestya village, st. Sportivna, bldg. 1"
h1.phone = "096-463-34-84"
h1.idp = 82
h1.contact_name = "Mykhailo"
h1.coordinator = co1
h1.region = r1

db_session.add(h1)
db_session.commit()


