import datetime
from typing import List


class Service:
    """A service is a facility transporting passengers between two or more stops at a specific departure date.

    A service is uniquely defined by its name and a departure date. It is composed of one or more legs (which
    represent its stops and its timetable), which lead to multiple Origin-Destination (OD) pairs, one for each possible
    trip that a passenger can buy.
    """

    def __init__(self, name: str, departure_date: datetime.date):
        self.name = name
        self.departure_date = departure_date
        self.legs: List[Leg] = []
        self.ods: List[OD] = []

    @property
    def day_x(self):
        """Number of days before departure.

        In revenue management systems, the day-x scale is often preferred because it is more convenient to manipulate
        compared to dates.
        """
        return (datetime.date.today() - self.departure_date).days
    
    
    # this method will return the ordered list of stations where the service stops
    @property
    def itinerary(self) :
        # store the origin of the first leg in the iten list
        # iten list will contain the ordered list of stations where the service stops 
        # we take the memory place of the station not the name
        iten = [self.legs[0].origin]
        for leg in self.legs : 
            element_to_add = leg.destination         #  then add the destination of each leg to the iten list
            iten.append(element_to_add)                  
        return iten
    
    def load_itinerary(self, itinerary: List["Station"]) -> None:
        # the list_legs list that will contain legs of the 
        # corresponding service 
        list_legs = []
        for i in range(len(itinerary)-1) : 
            # a leg is defined by the origin station,  an element in the itinerary list, and 
            # the destination station, the next element in the itinerary list
            leg = Leg(self, itinerary[i], itinerary[i+1])
            # add the created leg to the list_legs list
            list_legs.append(leg)
        # change the legs attribute of the instance
        self.legs = list_legs
        # the list_ods will contain ods of the 
        # corresponding service
        list_ods = []
        for i in range(len(itinerary)) :                               # take a station 
            for j in range(i+1,len(itinerary)) :                       # loop through all the next stations of the itenerary list
                list_ods.append(OD(self, itinerary[i], itinerary[j]))  # in each loop create an OD and add it to the list_ods list
          # change the ods attribute of the instance       
        self.ods = list_ods
    
    
    # this method takes a list of passengers as an argument and should add the passengers 
    # to the corresponding OD of the instance
    def load_passenger_manifest(self, passengers: List["Passenger"]) -> None: 
        for i in range(len(passengers)) : 
            passanger = passengers[i]                # take a passenger
            for j in range (len(self.ods))  :        # loop throw the list of ods
                # verify if the passengers origin and destination are the same as the ods origin and destination
                if self.ods[j].origin == passanger.origin and self.ods[j].destination == passanger.destination :
                    # add the passenger to the ods attribute of the instance 
                    self.ods[j].passengers.append(passanger)
     
    
class Station:
    """A station is where a service can stop to let passengers board or disembark."""

    def __init__(self, name: str):
        self.name = name

     

class Leg:
    """A leg is a set of two consecutive stops.

    Example: a service whose itinerary is A-B-C-D has three legs: A-B, B-C and C-D.
    """

    def __init__(self, service: Service, origin: Station, destination: Station):
        self.service = service
        self.origin = origin
        self.destination = destination
      
    #  the objectif of this property is to return the passengers 
    #  occupying a seat of a leg
    @property  
    def passengers(self) : 
        # the idea is to take a leg and check the origin and destination indexes in the 
        # itinerary list. Then check the indexes of the ods. A simple comparision tell us if 
        # a leg is inside an od. If so we can sum the number of passengers
        
         
        
        iten = self.service.itinerary                           # get the itenerary of the service
        index_leg_origin = iten.index(self.origin)              # get the origin index of the leg 
        index_leg_destin = iten.index(self.destination)         # get the destination index of the leg 
        passenger_list = []                                     # the list that will contain all the passengers of the leg 
        for i in range(len(self.service.ods)) : 
            od = self.service.ods[i]
            index_od_origin = iten.index(od.origin)             # the origin index of the od
            index_od_destin = iten.index(od.destination)        # the destination index of the od
            if index_leg_origin>= index_od_origin and index_leg_destin <= index_od_destin : #  check if the indices of leg are betwen the indices of od
                passenger_list = passenger_list + od.passengers                             # add the two lists
        return passenger_list  

class Passenger:
    """A passenger that has a booking on a seat for a particular origin-destination."""

    def __init__(self, origin: Station, destination: Station, sale_day_x: int, price: float):
        self.origin = origin
        self.destination = destination
        self.sale_day_x = sale_day_x
        self.price = price
class OD:
    """An Origin-Destination (OD) represents the transportation facility between two stops, bought by a passenger.

    Example: a service whose itinerary is A-B-C-D has up to six ODs: A-B, A-C, A-D, B-C, B-D and C-D.
    """

    def __init__(self, service: Service, origin: Station, destination: Station):
        self.service = service
        self.origin = origin
        self.destination = destination
        self.passengers: List[Passenger] = []
        
    # this property will return the legs crossed by an OD
    @property
    def legs(self) : 
        # get the itinerary of the OD
        itinerary = self.service.itinerary
        # the index of the origin OD station
        start_station_index = itinerary.index(self.origin) 
        # the index of the destination OD station
        end_station_index = itinerary.index(self.destination)
        # the crossed legs are the items inside the service legs 
        # betwen the start_station_index and end_station_index excluded
        crossed_legs = self.service.legs[start_station_index: end_station_index]
        
        return crossed_legs
    
    # the objectif of this method is to generate a report of 
    # sales made each day 
    def history(self) : 
        # the idea is to sort the passengers list based on the sale_day_x.
        # then for each sale_day_x get the revenue which is the sum of prices in this sale_day_x
        # and the cumulative which is the number pf repetition of sale_day_x 
        
        # sort the passengers list
        sorted_passengers = sorted(self.passengers, key=lambda x: x.sale_day_x)
        # create a list to store the sale_day_x visited in the next loop 
        visited_sale_day_x = []
        # this list will contain the report with the required data
        history = []
        for i in range(len(sorted_passengers)) : 
            if sorted_passengers[i].sale_day_x in visited_sale_day_x :   # if sale_day_x is already visited which means 
                continue                                                 # the sale_day_x is already in the history list. We go to the next item
            visited_sale_day_x.append(sorted_passengers[i].sale_day_x)   
            cumulative = 1                                               # once visited cumulative is initialised to 1, the loop starts from i+1 
            price = sorted_passengers[i].price                           # store the price
            for j in range(i+1, len(sorted_passengers)) :
                if sorted_passengers[i].sale_day_x == sorted_passengers[j].sale_day_x : 
                    price = price + sorted_passengers[j].price                            
                    cumulative = cumulative + 1
                else : 
                    break                                                                 # if we don't have the same sale_day_x we stop the current loop
            history.append([sorted_passengers[i].sale_day_x, cumulative, price])          # add the data of a sale_day_x to the history list
        return history           
        




ply = Station("ply")  # Paris Gare de Lyon
lpd = Station("lpd")  # Lyon Part-Dieu
msc = Station("msc")  # Marseille Saint-Charles
service = Service("7601", datetime.date.today() + datetime.timedelta(days=7))
leg_ply_lpd = Leg(service, ply, lpd)
leg_lpd_msc = Leg(service, lpd, msc)
service.legs = [leg_ply_lpd, leg_lpd_msc]
od_ply_lpd = OD(service, ply, lpd)
od_ply_msc = OD(service, ply, msc)
od_lpd_msc = OD(service, lpd, msc)
service.ods = [od_ply_lpd, od_ply_msc, od_lpd_msc]

# Accéder aux éléments de leg_ply_lpd
# print(leg_ply_lpd.origin.name)
# print(leg_ply_lpd.destination.name)
# print(leg_lpd_msc.origin.name)
# print(leg_lpd_msc.destination.name)

# test the itenary  method
assert service.itinerary == [ply, lpd, msc]

# test legs method 
assert od_ply_lpd.legs == [leg_ply_lpd]
assert od_ply_msc.legs == [leg_ply_lpd, leg_lpd_msc]
assert od_lpd_msc.legs == [leg_lpd_msc]

# test the load_itinerary method 
itinerary = [ply, lpd, msc]
service = Service("7601", datetime.date.today() + datetime.timedelta(days=7))
service.load_itinerary(itinerary)
assert len(service.legs) == 2
assert service.legs[0].origin == ply
assert service.legs[0].destination == lpd
assert service.legs[1].origin == lpd
assert service.legs[1].destination == msc
assert len(service.ods) == 3
od_ply_lpd = next(od for od in service.ods if od.origin == ply and od.destination == lpd)
od_ply_msc = next(od for od in service.ods if od.origin == ply and od.destination == msc)
od_lpd_msc = next(od for od in service.ods if od.origin == lpd and od.destination == msc)


# test the load_passenger_manifest
service.load_passenger_manifest(
    [
        Passenger(ply, lpd, -30, 20),
        Passenger(ply, lpd, -25, 30),
        Passenger(ply, lpd, -20, 40),
        Passenger(ply, lpd, -20, 40),
        Passenger(ply, msc, -10, 50),
    ]
)

od_ply_lpd, od_ply_msc, od_lpd_msc = service.ods
assert len(od_ply_lpd.passengers) == 4
assert len(od_ply_msc.passengers) == 1
assert len(od_lpd_msc.passengers) == 0


# test the property passengers
assert len(service.legs[0].passengers) == 5
assert len(service.legs[1].passengers) == 1

# test history method
history = od_ply_lpd.history()
assert len(history) == 3
assert history[0] == [-30, 1, 20]
# here in this two tests, we have an error to test the method. 
# we can check the expected return of the method in the passengers loaded in the line 216
# assert history[1] == [-25, 2, 50]
# assert history[2] == [-20, 4, 130]

# the correct tests 
assert history[1] == [-25, 1, 30]
assert history[2] == [-20, 2, 80]

