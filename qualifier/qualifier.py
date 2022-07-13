import typing
from dataclasses import dataclass

def get_staff(staff, speciality):
    """Get a list of staff with a given speciality.

    :param staff: list of staff
    :param speciality: speciality to look for
    :return: list of staff with the given speciality
    """
    for i in staff.values():
        for j in i.scope["speciality"]:
            if j == speciality:
                return i

@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        if request.scope["type"] == "staff.onduty":
            self.staff[request.scope["id"]] = request
        
        if request.scope["type"] == "staff.offduty":
            del self.staff[request.scope["id"]]

        if request.scope["type"] == "order":
            found = get_staff(self.staff, request.scope["speciality"])
            order = await request.receive()
            await found.send(order)
            result = await found.receive()
            await request.send(result)
        ...
